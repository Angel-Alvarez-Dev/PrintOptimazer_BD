# app/tasks/maintenance_tasks.py
"""
Maintenance and cleanup tasks
"""
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from celery import current_app
from app.core.celery import celery_app
from app.core.database import SessionLocal
from app.services.analytics_service import AnalyticsService
from app.models.models import ModelFile, InventoryTransaction
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=2)
def cleanup_old_files_task(self, days_old: int = 30):
    """Clean up old temporary files"""
    try:
        uploads_dir = Path("uploads")
        temp_dir = uploads_dir / "temp"
        
        if not temp_dir.exists():
            return {"status": "success", "message": "No temp directory found"}
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        deleted_size = 0
        
        for file_path in temp_dir.rglob("*"):
            if file_path.is_file():
                file_stat = file_path.stat()
                file_modified = datetime.fromtimestamp(file_stat.st_mtime)
                
                if file_modified < cutoff_date:
                    deleted_size += file_stat.st_size
                    file_path.unlink()
                    deleted_count += 1
        
        # Clean up empty directories
        for dir_path in temp_dir.rglob("*"):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                dir_path.rmdir()
        
        logger.info(f"Cleaned up {deleted_count} files ({deleted_size / 1024 / 1024:.2f} MB)")
        
        return {
            "status": "success",
            "deleted_files": deleted_count,
            "deleted_size_mb": deleted_size / 1024 / 1024
        }
        
    except Exception as exc:
        logger.error(f"File cleanup failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=3600)  # 1 hour delay
        
        return {"status": "failed", "error": str(exc)}

@celery_app.task(bind=True, max_retries=2)
def backup_database_task(self):
    """Create database backup"""
    try:
        from scripts.backup_db import create_backup
        
        backup_file = create_backup()
        
        if backup_file:
            logger.info(f"Database backup created: {backup_file}")
            return {"status": "success", "backup_file": backup_file}
        else:
            raise Exception("Backup creation failed")
        
    except Exception as exc:
        logger.error(f"Database backup failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=3600)
        
        return {"status": "failed", "error": str(exc)}

@celery_app.task(bind=True, max_retries=2)
def generate_daily_analytics_task(self):
    """Generate daily analytics reports"""
    try:
        db = SessionLocal()
        analytics_service = AnalyticsService(db)
        
        # Get all active users
        from app.models.models import User
        users = db.query(User).filter(User.is_active == True).all()
        
        reports = []
        for user in users:
            try:
                stats = analytics_service.get_dashboard_stats(user.id)
                project_stats = analytics_service.get_project_stats(user.id)
                material_stats = analytics_service.get_material_stats(user.id)
                
                report = {
                    "user_id": user.id,
                    "date": datetime.now().date().isoformat(),
                    "dashboard_stats": stats,
                    "project_stats": project_stats,  
                    "material_stats": material_stats
                }
                
                reports.append(report)
                
            except Exception as e:
                logger.error(f"Analytics generation failed for user {user.id}: {e}")
        
        # Save reports to file or database
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"daily_analytics_{datetime.now().date().isoformat()}.json"
        
        import json
        with open(report_file, 'w') as f:
            json.dump(reports, f, indent=2, default=str)
        
        logger.info(f"Daily analytics generated for {len(users)} users")
        
        return {
            "status": "success",
            "users_processed": len(users),
            "report_file": str(report_file)
        }
        
    except Exception as exc:
        logger.error(f"Daily analytics generation failed: {exc}")
        
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=3600)
        
        return {"status": "failed", "error": str(exc)}
    
    finally:
        db.close()