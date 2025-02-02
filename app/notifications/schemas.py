from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    message: str
    notification_type: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    status: str
    user_id: int

    class Config:
        orm_mode = True
