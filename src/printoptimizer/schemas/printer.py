"""Schemas para el modelo Printer."""

from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field, IPvAnyAddress, constr

from printoptimizer.schemas.base import BaseSchema, IDSchema, TimestampSchema
from printoptimizer.models.printer import PrinterStatus, PrinterType


class PrinterBase(BaseSchema):
    """Schema base para Printer."""
    
    name: constr(min_length=1, max_length=100)
    model: constr(min_length=1, max_length=100)
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    printer_type: PrinterType
    location: Optional[str] = None
    department: Optional[str] = None
    floor: Optional[int] = Field(None, ge=0)
    ip_address: Optional[str] = None
    mac_address: Optional[constr(pattern=r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')] = None
    hostname: Optional[str] = None
    color_printing: bool = False
    duplex_printing: bool = False
    max_paper_width: Optional[float] = Field(None, gt=0)
    max_paper_height: Optional[float] = Field(None, gt=0)
    priority: int = Field(5, ge=1, le=10)


class PrinterCreate(PrinterBase):
    """Schema para crear una impresora."""
    
    pass


class PrinterUpdate(BaseSchema):
    """Schema para actualizar una impresora."""
    
    name: Optional[constr(min_length=1, max_length=100)] = None
    model: Optional[constr(min_length=1, max_length=100)] = None
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    printer_type: Optional[PrinterType] = None
    status: Optional[PrinterStatus] = None
    location: Optional[str] = None
    department: Optional[str] = None
    floor: Optional[int] = Field(None, ge=0)
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    color_printing: Optional[bool] = None
    duplex_printing: Optional[bool] = None
    max_paper_width: Optional[float] = Field(None, gt=0)
    max_paper_height: Optional[float] = Field(None, gt=0)
    priority: Optional[int] = Field(None, ge=1, le=10)
    is_active: Optional[bool] = None


class PrinterInDB(PrinterBase, IDSchema, TimestampSchema):
    """Schema de impresora en base de datos."""
    
    status: PrinterStatus
    is_active: bool
    total_pages_printed: int
    total_jobs_completed: int


class Printer(PrinterInDB):
    """Schema de impresora para respuestas API."""
    
    is_available: bool
    
    @classmethod
    def from_orm_with_computed(cls, db_obj):
        """Crear instancia con campos computados."""
        return cls(
            **db_obj.__dict__,
            is_available=db_obj.is_available
        )


class PrinterList(BaseSchema):
    """Schema para lista de impresoras."""
    
    items: List[Printer]
    total: int
    page: int
    page_size: int
    pages: int
