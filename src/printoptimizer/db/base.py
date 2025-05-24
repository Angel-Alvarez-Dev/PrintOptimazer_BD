"""Configuración base de SQLAlchemy."""

from sqlalchemy.ext.declarative import declarative_base

# Base para todos los modelos
Base = declarative_base()

# Importar todos los modelos aquí para que Alembic los detecte
# from printoptimizer.models.printer import Printer  # noqa
# from printoptimizer.models.job import Job  # noqa
