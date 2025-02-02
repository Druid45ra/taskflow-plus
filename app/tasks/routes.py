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
    
    # Trimite notificări
    notification_service = NotificationService()
    await notification_service.send_websocket_notification(
        user_id=db_task.owner_id,
        message=f"New task created: {db_task.title}"
    )
    
    # Trimite email (exemplu)
    user = db.query(User).filter(User.id == db_task.owner_id).first()
    if user:
        await notification_service.send_email(
            to_email=user.email,
            subject="New Task Assigned",
            content=f"You have a new task: {db_task.title}"
        )
    
    return db_task

router = APIRouter(prefix="/tasks", tags=["tasks"])
active_connections = []

# WebSocket endpoint pentru actualizări live
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

# Funcție helper pentru broadcast mesaje
async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    # Trimite notificare prin WebSocket
    broadcast(f"Task creat: {db_task.title}")
    return db_task

# În app/tasks/routes.py
@router.post("/", response_model=schemas.TaskResponse)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Trimite update la owner
    task_data = schemas.TaskResponse.from_orm(db_task).dict()
    await services.send_task_update(task_data, db_task.owner_id)
    
    # Broadcast la admini/manageri
    await services.broadcast_task_creation(task_data)
    
    return db_task
