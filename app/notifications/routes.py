from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from . import schemas, models
from .services import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])
service = NotificationService()

@router.post("/send-email", response_model=schemas.NotificationResponse)
async def send_email_notification(email_data: schemas.NotificationCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == email_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await service.send_email(
        to_email=user.email,
        subject="New Notification",
        content=f"<strong>{email_data.message}</strong>"
    )
    return {"id": 1, "created_at": datetime.now(), "status": "sent", "user_id": email_data.user_id}  # Example response

@router.get("/user/{user_id}", response_model=list[schemas.NotificationResponse])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).all()
