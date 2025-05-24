"""Configuración de la sesión de base de datos."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from printoptimizer.core.config import get_settings

settings = get_settings()

# Crear engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Crear SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener sesión de DB.
    
    Yields:
        Session: Sesión de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
