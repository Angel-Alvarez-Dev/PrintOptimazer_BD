"""Schemas base para la aplicación."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Schema base con configuración común."""
    
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class TimestampSchema(BaseSchema):
    """Schema con timestamps."""
    
    created_at: datetime
    updated_at: datetime


class IDSchema(BaseSchema):
    """Schema con ID."""
    
    id: int
