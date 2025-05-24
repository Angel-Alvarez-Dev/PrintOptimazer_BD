"""Mixins para modelos de base de datos."""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped


class TimestampMixin:
    """Mixin para agregar timestamps a los modelos."""
    
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        )
    
    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )


class IDMixin:
    """Mixin para agregar ID autoincremental."""
    
    @declared_attr
    def id(cls) -> Mapped[int]:
        return Column(Integer, primary_key=True, autoincrement=True)
