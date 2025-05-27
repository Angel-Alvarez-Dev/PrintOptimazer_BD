# app/tasks/ai_tasks.py

from app.core.celery import celery_app
from app.services.ai_service import AIService
from app.db.session import SessionLocal
from app.db.models import ModelMetadata
from app.schemas.ai_task import PrintTimeRequest

@celery_app.task(name="app.tasks.generate_seo_title_task")
def generate_seo_title_task(model_id: str) -> None:
    """Genera y guarda el título SEO para un modelo."""
    service = AIService()
    title = service.generate_seo_title(model_id)
    db = SessionLocal()
    try:
        meta = db.query(ModelMetadata).filter_by(model_id=model_id).first()
        if not meta:
            meta = ModelMetadata(model_id=model_id)
            db.add(meta)
        meta.seo_title = title
        db.commit()
    finally:
        db.close()

@celery_app.task(name="app.tasks.generate_market_description_task")
def generate_market_description_task(model_id: str) -> None:
    """Genera y guarda la descripción optimizada para marketplaces."""
    service = AIService()
    desc = service.generate_market_description(model_id)
    db = SessionLocal()
    try:
        meta = db.query(ModelMetadata).filter_by(model_id=model_id).first()
        if not meta:
            meta = ModelMetadata(model_id=model_id)
            db.add(meta)
        meta.market_description = desc
        db.commit()
    finally:
        db.close()

@celery_app.task(name="app.tasks.generate_tags_task")
def generate_tags_task(model_id: str) -> None:
    """Genera y guarda los tags inteligentes basados en contenido."""
    service = AIService()
    tags = service.generate_tags(model_id)
    db = SessionLocal()
    try:
        meta = db.query(ModelMetadata).filter_by(model_id=model_id).first()
        if not meta:
            meta = ModelMetadata(model_id=model_id)
            db.add(meta)
        meta.tags = tags
        db.commit()
    finally:
        db.close()

@celery_app.task(name="app.tasks.analyze_complexity_task")
def analyze_complexity_task(model_file_url: str, model_id: str) -> None:
    """Analiza la complejidad del modelo y guarda el reporte."""
    service = AIService()
    report = service.analyze_complexity(model_file_url)
    db = SessionLocal()
    try:
        meta = db.query(ModelMetadata).filter_by(model_id=model_id).first()
        if not meta:
            meta = ModelMetadata(model_id=model_id)
            db.add(meta)
        meta.vertices = report.vertices
        meta.polygons = report.polygons
        meta.file_size_kb = report.file_size_kb
        meta.complexity_score = report.complexity_score
        db.commit()
    finally:
        db.close()

@celery_app.task(name="app.tasks.predict_print_time_task")
def predict_print_time_task(request_dict: dict, model_id: str) -> None:
    """Predice y guarda el tiempo de impresión."""
    req = PrintTimeRequest(**request_dict)
    service = AIService()
    result = service.predict_print_time(req)
    db = SessionLocal()
    try:
        meta = db.query(ModelMetadata).filter_by(model_id=model_id).first()
        if not meta:
            meta = ModelMetadata(model_id=model_id)
            db.add(meta)
        meta.estimated_time_minutes = result.estimated_time_minutes
        db.commit()
    finally:
        db.close()
