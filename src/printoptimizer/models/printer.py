"""Modelo de Impresora."""

from typing import TYPE_CHECKING, List, Optional
from enum import Enum

from sqlalchemy import Boolean, Column, Enum as SQLEnum, Float, Integer, String, Text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm.relationships import RelationshipProperty

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
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)
    model: Mapped[str] = Column(String(100), nullable=False)
    manufacturer: Mapped[Optional[str]] = Column(String(100))
    serial_number: Mapped[Optional[str]] = Column(String(100), unique=True)
    
    # Tipo y estado
    printer_type: Mapped[PrinterType] = Column(SQLEnum(PrinterType), nullable=False)
    status: Mapped[PrinterStatus] = Column(
        SQLEnum(PrinterStatus),
        nullable=False,
        default=PrinterStatus.OFFLINE,
    )
    
    # Ubicación
    location: Mapped[Optional[str]] = Column(String(200))
    department: Mapped[Optional[str]] = Column(String(100))
    floor: Mapped[Optional[int]] = Column(Integer)
    
    # Configuración de red
    ip_address: Mapped[Optional[str]] = Column(String(45))  # Soporta IPv4 e IPv6
    mac_address: Mapped[Optional[str]] = Column(String(17))
    hostname: Mapped[Optional[str]] = Column(String(255))
    
    # Capacidades
    color_printing: Mapped[bool] = Column(Boolean, default=False)
    duplex_printing: Mapped[bool] = Column(Boolean, default=False)
    max_paper_width: Mapped[Optional[float]] = Column(Float)  # en mm
    max_paper_height: Mapped[Optional[float]] = Column(Float)  # en mm
    supported_paper_sizes: Mapped[Optional[str]] = Column(Text)  # JSON array
    
    # Estadísticas
    total_pages_printed: Mapped[int] = Column(Integer, default=0)
    total_jobs_completed: Mapped[int] = Column(Integer, default=0)
    
    # Configuración
    is_active: Mapped[bool] = Column(Boolean, default=True)
    priority: Mapped[int] = Column(Integer, default=5)  # 1-10, mayor = más prioridad
    
    # Relaciones - comentada por ahora hasta crear el modelo PrintJob
    # print_jobs: Mapped[List["PrintJob"]] = relationship(
    #     "PrintJob",
    #     back_populates="printer",
    #     cascade="all, delete-orphan",
    # )
    
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
