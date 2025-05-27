# app/tasks/__init__.py
"""
Background tasks for PrintOptimizer
"""
from .email_tasks import send_email_task, send_quote_email_task
from .ai_tasks import generate_ai_metadata_task, analyze_model_complexity_task
from .sync_tasks import sync_marketplace_data_task, sync_user_marketplace_data_task
from .maintenance_tasks import cleanup_old_files_task, backup_database_task, generate_daily_analytics_task

__all__ = [
    'send_email_task',
    'send_quote_email_task', 
    'generate_ai_metadata_task',
    'analyze_model_complexity_task',
    'sync_marketplace_data_task',
    'sync_user_marketplace_data_task',
    'cleanup_old_files_task',
    'backup_database_task',
    'generate_daily_analytics_task'
]
