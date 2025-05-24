"""Router principal de la API v1."""

from fastapi import APIRouter

from printoptimizer.api.v1.endpoints import printers

api_router = APIRouter()

# Incluir rutas
api_router.include_router(
    printers.router,
    prefix="/printers",
    tags=["printers"],
)
