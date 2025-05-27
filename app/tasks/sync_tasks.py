# app/tasks/sync_tasks.py
"""
Data synchronization tasks
"""
from celery import current_app
from app.core.celery import celery_app
from app.services.marketplace_service import MarketplaceService
from app.core.database import SessionLocal
from app.models.models import User
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def sync_marketplace_data_task(self):
    """Sync marketplace data for all users"""
    try:
        db = SessionLocal()
        
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()
        
        marketplace_service = MarketplaceService(db)
        
        results = []
        for user in users:
            try:
                stats = marketplace_service.sync_marketplace_stats(user.id)
                results.append({"user_id": user.id, "stats": stats})
            except Exception as e:
                logger.error(f"Sync failed for user {user.id}: {e}")
                results.append({"user_id": user.id, "error": str(e)})
        
        logger.info(f"Marketplace sync completed for {len(users)} users")
        return {"status": "success", "results": results}
        
    except Exception as exc:
        logger.error(f"Marketplace sync task failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=300)
        
        return {"status": "failed", "error": str(exc)}
    
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3)
def sync_user_marketplace_data_task(self, user_id: int):
    """Sync marketplace data for specific user"""
    try:
        db = SessionLocal()
        marketplace_service = MarketplaceService(db)
        
        stats = marketplace_service.sync_marketplace_stats(user_id)
        
        logger.info(f"Marketplace sync completed for user {user_id}")
        return {"status": "success", "user_id": user_id, "stats": stats}
        
    except Exception as exc:
        logger.error(f"User marketplace sync failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=300)
        
        return {"status": "failed", "error": str(exc)}
    
    finally:
        db.close()