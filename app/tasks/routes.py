from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from ..core.database import get_db
from . import schemas, models
from ..users.models import User

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
