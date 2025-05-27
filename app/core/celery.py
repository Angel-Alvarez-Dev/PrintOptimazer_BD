# app/core/celery.py
"""
Celery configuration for background tasks
"""
from celery import Celery
from app.core.config import settings
import os

# Create Celery instance
celery_app = Celery(
    "printoptimizer",
    broker=settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else "redis://localhost:6379/0",
    backend=settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else "redis://localhost:6379/0",
    include=["app.tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone='UTC',
    enable_utc=True,
    task_routes={
        'app.tasks.send_email': {'queue': 'emails'},
        'app.tasks.generate_ai_metadata': {'queue': 'ai'},
        'app.tasks.sync_marketplace_data': {'queue': 'sync'},
        'app.tasks.cleanup_old_files': {'queue': 'maintenance'},
    },
    beat_schedule={
        'sync-marketplace-data': {
            'task': 'app.tasks.sync_marketplace_data',
            'schedule': 300.0,  # Every 5 minutes
        },
        'cleanup-old-files': {
            'task': 'app.tasks.cleanup_old_files',
            'schedule': 86400.0,  # Daily
        },
        'generate-analytics-reports': {
            'task': 'app.tasks.generate_daily_analytics',
            'schedule': 86400.0,  # Daily at midnight
        },
        'backup-database': {
            'task': 'app.tasks.backup_database',
            'schedule': 86400.0 * 7,  # Weekly
        },
    }
)