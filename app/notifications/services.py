import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..core.config import settings
from ..core.database import SessionLocal
from .models import Notification

class NotificationService:
    def __init__(self):
        self.sg_client = SendGridAPIClient(api_key=settings.sendgrid_api_key)
    
    async def send_email(self, to_email: str, subject: str, content: str):
        message = Mail(
            from_email=settings.email_sender,
            to_emails=to_email,
            subject=subject,
            html_content=content
        )
        try:
            response = self.sg_client.send(message)
            self._log_notification(to_email, "email", "sent")
            return response.status_code
        except Exception as e:
            self._log_notification(to_email, "email", "failed", str(e))
            raise e
    
    async def send_websocket_notification(self, user_id: int, message: str):
        from ..tasks.routes import active_connections  # Import circular gestionat
        db = SessionLocal()
        try:
            # Trimite mesajul la toate conexiunile active ale user-ului
            for ws in active_connections:
                if ws.user_id == user_id:  # Presupunem că conexiunile WebSocket au user_id
                    await ws.send_text(message)
            self._log_notification(user_id, "websocket", "sent")
        except Exception as e:
            self._log_notification(user_id, "websocket", "failed", str(e))
            raise e
        finally:
            db.close()
    
    def _log_notification(self, recipient: str | int, notification_type: str, status: str, error_msg: str = None):
        db = SessionLocal()
        try:
            notification = Notification(
                user_id=recipient if isinstance(recipient, int) else None,
                message=error_msg or "Notification sent",
                notification_type=notification_type,
                status=status
            )
            db.add(notification)
            db.commit()
        finally:
            db.close()
