"""
Email-related background tasks
"""
from celery import current_app
from app.core.celery import celery_app
from app.services.notification_service import NotificationService
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, to_email: str, subject: str, body: str, attachments: list = None):
    """Send email task"""
    try:
        db = SessionLocal()
        notification_service = NotificationService(db)
        
        success = notification_service.send_email(to_email, subject, body, attachments)
        
        if not success:
            raise Exception("Email sending failed")
        
        logger.info(f"Email sent successfully to {to_email}")
        return {"status": "success", "recipient": to_email}
        
    except Exception as exc:
        logger.error(f"Email sending failed: {exc}")
        
        # Retry with exponential backoff
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60 * (2 ** self.request.retries))
        
        return {"status": "failed", "error": str(exc)}
    
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3)
def send_quote_email_task(self, quote_id: int, user_id: int):
    """Send quote email task"""
    try:
        db = SessionLocal()
        notification_service = NotificationService(db)
        
        success = notification_service.send_quote_email(quote_id, user_id)
        
        if not success:
            raise Exception("Quote email sending failed")
        
        logger.info(f"Quote email sent successfully for quote {quote_id}")
        return {"status": "success", "quote_id": quote_id}
        
    except Exception as exc:
        logger.error(f"Quote email sending failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60 * (2 ** self.request.retries))
        
        return {"status": "failed", "error": str(exc)}
    
    finally:
        db.close()
