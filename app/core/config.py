from pydantic import BaseSettings, AnyUrl
from typing import List

class Settings(BaseSettings):
    # Conexión a BD
    DATABASE_URL: AnyUrl
    # Redis para Celery
    REDIS_URL: AnyUrl
    # Servicio de IA
    OPENAI_API_KEY: str
    # Autenticación
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # Orígenes CORS
    CORS_ORIGINS: List[str] = []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Única instancia de settings en toda la aplicación
settings = Settings()
