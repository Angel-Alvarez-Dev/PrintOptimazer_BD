"""Aplicación principal FastAPI."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from printoptimizer.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Contexto de vida de la aplicación.
    
    Args:
        app: Instancia de FastAPI.
        
    Yields:
        None
    """
    # Startup
    print("🚀 Iniciando PrintOptimizer BD...")
    yield
    # Shutdown
    print("👋 Cerrando PrintOptimizer BD...")


def create_app() -> FastAPI:
    """
    Crear y configurar la aplicación FastAPI.
    
    Returns:
        FastAPI: Aplicación configurada.
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Rutas de health check
    @app.get("/")
    async def root():
        """Ruta raíz."""
        return {
            "message": "Welcome to PrintOptimizer BD",
            "version": settings.version,
            "docs": "/docs",
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": settings.version}
    
    return app


app = create_app()
