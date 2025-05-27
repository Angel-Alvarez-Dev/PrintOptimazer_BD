# app/core/celery.py
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Instancia de Celery
celery_app = Celery(
    "printoptimizer",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"]
)

# Configuración de mensajería asíncrona
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone='America/Mexico_City',
    enable_utc=False,
    task_routes={
        'app.tasks.send_email': {'queue': 'emails'},
        'app.tasks.generate_ai_metadata': {'queue': 'ai'},
        'app.tasks.sync_marketplace_data': {'queue': 'sync'},
        'app.tasks.cleanup_old_files': {'queue': 'maintenance'},
    },
    beat_schedule={
        # Cada 5 minutos
        'sync-marketplace-data': {
            'task': 'app.tasks.sync_marketplace_data',
            'schedule': 300.0,
        },
        # A medianoche local todos los días
        'cleanup-old-files': {
            'task': 'app.tasks.cleanup_old_files',
            'schedule': crontab(hour=0, minute=0),
        },
        # Reporte diario de analíticas a medianoche
        'generate-daily-analytics': {
            'task': 'app.tasks.generate_daily_analytics',
            'schedule': crontab(hour=0, minute=0),
        },
        # Backup semanal los domingos a medianoche
        'backup-database': {
            'task': 'app.tasks.backup_database',
            'schedule': crontab(day_of_week='sun', hour=0, minute=0),
        },
    }
)