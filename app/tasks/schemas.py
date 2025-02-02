from datetime import datetime
from pydantic import BaseModel
from ..users.schemas import UserInDB

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    deadline: datetime
    priority: str = "Medium"
    status: str = "Pending"

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    owner: UserInDB
    
    class Config:
        orm_mode = True