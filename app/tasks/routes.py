from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from ..core.database import get_db
from . import schemas, models
from ..users.models import User
from ..notifications.services import NotificationService
from fastapi import APIRouter, Depends, WebSocket, Query
from ..core.websocket_manager import manager
from ..core.security import verify_jwt_token
from ..core.config import settings
from ..tasks import services  # Ensure services is imported

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    try:
        payload = verify_jwt_token(token, settings.jwt_secret, settings.jwt_algorithm)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            # Păstrează conexiunea deschisă cu un heartbeat
            await websocket.receive_text()
    except:
        manager.disconnect(websocket, user_id)

@router.post("/", response_model=schemas.TaskResponse)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Send notifications
    notification_service = NotificationService()
    await notification_service.send_websocket_notification(
        user_id=db_task.owner_id,
        message=f"New task created: {db_task.title}"
    )
    
    # Send email (example)
    user = db.query(User).filter(User.id == db_task.owner_id).first()
    if user:
        await notification_service.send_email(
            to_email=user.email,
            subject="New Task Assigned",
            content=f"You have a new task: {db_task.title}"
        )
    
    # Send task update and broadcast
    task_data = schemas.TaskResponse.from_orm(db_task).dict()
    await services.send_task_update(task_data, db_task.owner_id)
    await services.broadcast_task_creation(task_data)
    
    return db_task

router = APIRouter(prefix="/tasks", tags=["tasks"])
active_connections = []

# Funcție helper pentru broadcast mesaje
async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)
