from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from . import schemas, models
from ..users.models import User
from ..notifications.services import NotificationService
from .services import send_task_update, broadcast_task_creation

router = APIRouter(prefix="/tasks", tags=["tasks"])
notification_service = NotificationService()

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
    
    await broadcast_task_creation(new_task.dict())
    
    return new_task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict().items():
        setattr(existing_task, key, value)
    
    db.commit()
    db.refresh(existing_task)
    
    await send_task_update(existing_task.dict(), existing_task.owner_id)
    
    return existing_task

@router.get("/{task_id}", response_model=schemas.TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return {"detail": "Task deleted successfully"}
