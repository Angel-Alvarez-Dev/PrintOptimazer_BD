from pydantic import BaseSettings

class Settings(BaseSettings):
    # Configuración de la base de datos
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/printoptimizer_db"

    # Configuración de la aplicación
    APP_NAME: str = "PrintOptimizer_BD"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Configuración de autenticación (ejemplo)
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"  # Indica que las variables pueden definirse en un archivo .env

# Instancia de configuración
settings = Settings()
