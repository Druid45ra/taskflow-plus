from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    notification_type = Column(String)  # email, websocket, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # sent, failed
