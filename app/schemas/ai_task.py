# app/schemas/ai_task.py
from pydantic import BaseModel, Field
from typing import List, Optional


class AIRequest(BaseModel):
    model_id: str = Field(..., description="ID del modelo 3D para generar metadatos")


class MetadataResponse(BaseModel):
    title: str = Field(..., description="Título SEO generado")
    description: str = Field(..., description="Descripción optimizada para marketplaces")
    tags: List[str] = Field(..., description="Lista de tags inteligentes basados en contenido")


class ComplexityRequest(BaseModel):
    model_file_url: str = Field(..., description="URL o ruta del archivo del modelo 3D")


class ComplexityReport(BaseModel):
    vertices: int = Field(..., description="Número total de vértices")
    polygons: int = Field(..., description="Número total de polígonos")
    file_size_kb: float = Field(..., description="Tamaño del archivo en KB")
    complexity_score: float = Field(..., description="Puntuación de complejidad calculada")


class PrintTimeRequest(BaseModel):
    model_file_url: str = Field(..., description="URL o ruta del archivo del modelo 3D")
    material: str = Field(..., description="Tipo de material para impresión")
    layer_height_mm: float = Field(..., description="Altura de capa en mm")
    infill_percent: float = Field(..., description="Porcentaje de relleno")


class PrintTimeResponse(BaseModel):
    estimated_time_minutes: float = Field(..., description="Tiempo estimado de impresión en minutos")