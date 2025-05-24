"""Modelo de Impresora."""

from typing import TYPE_CHECKING, List, Optional
from enum import Enum

from sqlalchemy import Boolean, Column, Enum as SQLEnum, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from printoptimizer.models.base import Base

if TYPE_CHECKING:
    from printoptimizer.models.job import PrintJob


class PrinterStatus(str, Enum):
    """Estados posibles de una impresora."""
    
    ONLINE = "online"
    OFFLINE = "offline"
    PRINTING = "printing"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class PrinterType(str, Enum):
    """Tipos de impresora."""
    
    LASER = "laser"
    INKJET = "inkjet"
    THERMAL = "thermal"
    PLOTTER = "plotter"
    MULTIFUNCTIONAL = "multifunctional"


class Printer(Base):
    """Modelo de impresora."""
    
    __tablename__ = "printers"
    
    # Información básica
    name = Column(String(100), nullable=False, unique=True)
    model = Column(String(100), nullable=False)
    manufacturer = Column(String(100))
    serial_number = Column(String(100), unique=True)
    
    # Tipo y estado
    printer_type = Column(SQLEnum(PrinterType), nullable=False)
    status = Column(
        SQLEnum(PrinterStatus),
        nullable=False,
        default=PrinterStatus.OFFLINE,
    )
    
    # Ubicación
    location = Column(String(200))
    department = Column(String(100))
    floor = Column(Integer)
    
    # Configuración de red
    ip_address = Column(String(45))  # Soporta IPv4 e IPv6
    mac_address = Column(String(17))
    hostname = Column(String(255))
    
    # Capacidades
    color_printing = Column(Boolean, default=False)
    duplex_printing = Column(Boolean, default=False)
    max_paper_width = Column(Float)  # en mm
    max_paper_height = Column(Float)  # en mm
    supported_paper_sizes = Column(Text)  # JSON array
    
    # Estadísticas
    total_pages_printed = Column(Integer, default=0)
    total_jobs_completed = Column(Integer, default=0)
    
    # Configuración
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=5)  # 1-10, mayor = más prioridad
    
    # Relaciones
    print_jobs: List["PrintJob"] = relationship(
        "PrintJob",
        back_populates="printer",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        """Representación del objeto."""
        return f"<Printer(id={self.id}, name='{self.name}', status={self.status.value})>"
    
    @property
    def is_available(self) -> bool:
        """Verifica si la impresora está disponible para imprimir."""
        return (
            self.is_active
            and self.status in [PrinterStatus.ONLINE, PrinterStatus.PRINTING]
        )
