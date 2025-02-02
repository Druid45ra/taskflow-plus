from fastapi import APIRouter, Depends, HTTPException, WebSocket, Query, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from . import schemas, models
from ..users.models import User
from ..notifications.services import NotificationService
from ..core.websocket_manager import manager
from ..core.security import verify_jwt_token
from ..core.config import settings
from ..tasks import services  # Ensure services is imported

router = APIRouter(prefix="/tasks", tags=["tasks"])
notification_service = NotificationService()

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
            # Keep the connection open with a heartbeat
            await websocket.receive_text()
    except:
        manager.disconnect(websocket, user_id)

@router.post("/", response_model=schemas.TaskResponse)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == task.owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    await notification_service.send_email(
        to_email=user.email,
        subject="New Task Created",
        content=f"Task '{new_task.title}' has been created."
    )
    
    return new_task
