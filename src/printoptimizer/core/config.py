"""Configuración central de la aplicación."""

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic."""

    # Application
    app_name: str = "PrintOptimizer BD"
    app_env: str = "development"
    debug: bool = True
    version: str = "0.1.0"
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "postgresql://user:pass@localhost/db"
    db_echo: bool = False
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    backend_cors_origins: List[str] = ["http://localhost:3000"]
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    class Config:
        """Configuración de Pydantic."""
        
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Obtener instancia de configuración (cached).
    
    Returns:
        Settings: Configuración de la aplicación.
    """
    return Settings()
