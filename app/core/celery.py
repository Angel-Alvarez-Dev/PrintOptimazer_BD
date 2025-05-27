# app/core/celery.py
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings
import time
from celery.signals import task_prerun, task_postrun, task_failure
from app.core.metrics import CELERY_TASK_FAILURES, CELERY_TASK_DURATION

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

@task_prerun.connect
def _task_prerun_handler(sender=None, task_id=None, task=None, **kwargs):
    # Marca el inicio
    setattr(task, "_start_time", time.time())

@task_postrun.connect
def _task_postrun_handler(sender=None, task_id=None, task=None, **kwargs):
    # Calcula y registra la duración
    start = getattr(task, "_start_time", None)
    if start is not None:
        duration = time.time() - start
        CELERY_TASK_DURATION.labels(task_name=sender.name).observe(duration)

@task_failure.connect
def _task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    # Incrementa el contador de fallos
    CELERY_TASK_FAILURES.labels(task_name=sender.name).inc()