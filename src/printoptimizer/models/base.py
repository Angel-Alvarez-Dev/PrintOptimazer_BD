"""Modelo base para todos los modelos de la aplicación."""

from sqlalchemy.ext.declarative import declarative_base

from printoptimizer.models.mixins import IDMixin, TimestampMixin


class Base(IDMixin, TimestampMixin):
    """Clase base para todos los modelos."""
    
    __abstract__ = True


# Crear la base declarativa
Base = declarative_base(cls=Base)
