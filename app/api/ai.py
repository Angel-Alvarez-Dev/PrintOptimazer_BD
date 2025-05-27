# app/api/ai.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.ai_task import (
    ComplexityRequest,
    PrintTimeRequest,
    MetadataResponse,
    ComplexityReport,
    PrintTimeResponse,
)
from app.tasks.ai_tasks import (
    generate_seo_title_task,
    generate_market_description_task,
    generate_tags_task,
    analyze_complexity_task,
    predict_print_time_task,
)
from app.core.celery import celery_app
from app.db.session import SessionLocal
from app.db.models import ModelMetadata

router = APIRouter(prefix="/api/v1/ai", tags=["AI"])

@router.post(
    "/seo/{model_id}",
    response_model=MetadataResponse,
    summary="Encola generación de título SEO",
)
async def enqueue_seo(model_id: str):
    task = generate_seo_title_task.delay(model_id)
    return JSONResponse({"task_id": task.id, "status": "queued"})

@router.post(
    "/description/{model_id}",
    response_model=MetadataResponse,
    summary="Encola generación de descripción optimizada",
)
async def enqueue_description(model_id: str):
    task = generate_market_description_task.delay(model_id)
    return JSONResponse({"task_id": task.id, "status": "queued"})

@router.post(
    "/tags/{model_id}",
    response_model=MetadataResponse,
    summary="Encola generación de tags inteligentes",
)
async def enqueue_tags(model_id: str):
    task = generate_tags_task.delay(model_id)
    return JSONResponse({"task_id": task.id, "status": "queued"})

@router.post(
    "/complexity/{model_id}",
    response_model=ComplexityReport,
    summary="Encola análisis de complejidad de modelo",
)
async def enqueue_complexity(model_id: str, request: ComplexityRequest):
    task = analyze_complexity_task.delay(request.model_file_url, model_id)
    return JSONResponse({"task_id": task.id, "status": "queued"})

@router.post(
    "/print-time/{model_id}",
    response_model=PrintTimeResponse,
    summary="Encola predicción de tiempo de impresión",
)
async def enqueue_print_time(model_id: str, request: PrintTimeRequest):
    task = predict_print_time_task.delay(request.dict(), model_id)
    return JSONResponse({"task_id": task.id, "status": "queued"})

@router.get(
    "/result/{task_id}",
    response_model=MetadataResponse,  # o un esquema genérico que abarque todos los campos
    summary="Consulta resultado de tarea de IA",
)
async def get_ai_result(task_id: str):
    result = celery_app.AsyncResult(task_id)
    state = result.state

    if state in ("PENDING", "STARTED"):
        return {"task_id": task_id, "status": state}

    if state == "SUCCESS":
        db = SessionLocal()
        try:
            meta = db.query(ModelMetadata).filter_by(task_id=task_id).first()
            if not meta:
                raise HTTPException(status_code=404, detail="Result not found")
            return {
                "task_id": task_id,
                "status": state,
                "data": {
                    "model_id": meta.model_id,
                    "seo_title": meta.seo_title,
                    "market_description": meta.market_description,
                    "tags": meta.tags,
                    "vertices": meta.vertices,
                    "polygons": meta.polygons,
                    "file_size_kb": meta.file_size_kb,
                    "complexity_score": meta.complexity_score,
                    "estimated_time_minutes": meta.estimated_time_minutes,
                },
            }
        finally:
            db.close()

    if state == "FAILURE":
        return {"task_id": task_id, "status": state, "error": str(result.result)}

    return {"task_id": task_id, "status": state}
