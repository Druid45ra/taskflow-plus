from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    deadline = Column(DateTime)
    priority = Column(String, default="Medium")
    status = Column(String, default="Pending")
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="tasks")
