from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    deadline: datetime
    priority: str = "Medium"  # Valori: Urgent/High/Medium/Low
    status: str = "Pending"   # Valori: Pending/In Progress/Completed

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True  # Compatibil cu SQLAlchemy
