# app/tasks/ai_tasks.py
"""
AI-related background tasks
"""
from celery import current_app
from app.core.celery import celery_app
from app.services.ai_service import AIService
from app.services.file_service import FileService
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=2)
def generate_ai_metadata_task(self, file_id: int, platform: str, user_id: int):
    """Generate AI metadata task"""
    try:
        db = SessionLocal()
        ai_service = AIService()
        file_service = FileService(db)
        
        metadata = ai_service.generate_ai_metadata(file_id, platform, user_id)
        
        logger.info(f"AI metadata generated for file {file_id}")
        return {"status": "success", "file_id": file_id, "metadata": metadata}
        
    except Exception as exc:
        logger.error(f"AI metadata generation failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=300)  # 5 minute delay
        
        return {"status": "failed", "error": str(exc)}
    
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=2)
def analyze_model_complexity_task(self, file_path: str):
    """Analyze 3D model complexity task"""
    try:
        ai_service = AIService()
        analysis = ai_service.analyze_model_complexity(file_path)
        
        logger.info(f"Model complexity analyzed for {file_path}")
        return {"status": "success", "analysis": analysis}
        
    except Exception as exc:
        logger.error(f"Model complexity analysis failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=300)
        
        return {"status": "failed", "error": str(exc)}