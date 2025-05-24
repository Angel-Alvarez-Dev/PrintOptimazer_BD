"""Servicio para operaciones con impresoras."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from printoptimizer.models.printer import Printer, PrinterStatus
from printoptimizer.schemas.printer import PrinterCreate, PrinterUpdate


class PrinterService:
    """Servicio para gestionar impresoras."""
    
    def __init__(self, db: Session):
        """
        Inicializar servicio.
        
        Args:
            db: Sesión de base de datos.
        """
        self.db = db
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        status: Optional[PrinterStatus] = None,
    ) -> List[Printer]:
        """
        Obtener todas las impresoras con filtros opcionales.
        
        Args:
            skip: Número de registros a saltar.
            limit: Número máximo de registros a retornar.
            is_active: Filtrar por estado activo/inactivo.
            status: Filtrar por estado de la impresora.
            
        Returns:
            Lista de impresoras.
        """
        query = select(Printer)
        
        if is_active is not None:
            query = query.where(Printer.is_active == is_active)
        
        if status is not None:
            query = query.where(Printer.status == status)
        
        query = query.offset(skip).limit(limit)
        result = self.db.execute(query)
        return result.scalars().all()
    
    def get_by_id(self, printer_id: int) -> Optional[Printer]:
        """
        Obtener impresora por ID.
        
        Args:
            printer_id: ID de la impresora.
            
        Returns:
            Impresora si existe, None en caso contrario.
        """
        return self.db.get(Printer, printer_id)
    
    def create(self, printer_data: PrinterCreate) -> Printer:
        """
        Crear nueva impresora.
        
        Args:
            printer_data: Datos de la impresora.
            
        Returns:
            Impresora creada.
        """
        printer = Printer(**printer_data.model_dump())
        self.db.add(printer)
        self.db.commit()
        self.db.refresh(printer)
        return printer
    
    def update(
        self,
        printer_id: int,
        printer_data: PrinterUpdate
    ) -> Optional[Printer]:
        """
        Actualizar impresora.
        
        Args:
            printer_id: ID de la impresora.
            printer_data: Datos a actualizar.
            
        Returns:
            Impresora actualizada si existe, None en caso contrario.
        """
        printer = self.get_by_id(printer_id)
        if not printer:
            return None
        
        update_data = printer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(printer, field, value)
        
        self.db.commit()
        self.db.refresh(printer)
        return printer
    
    def delete(self, printer_id: int) -> bool:
        """
        Eliminar impresora.
        
        Args:
            printer_id: ID de la impresora.
            
        Returns:
            True si se eliminó, False si no existe.
        """
        printer = self.get_by_id(printer_id)
        if not printer:
            return False
        
        self.db.delete(printer)
        self.db.commit()
        return True
    
    def get_available_printers(self) -> List[Printer]:
        """
        Obtener impresoras disponibles para imprimir.
        
        Returns:
            Lista de impresoras disponibles.
        """
        query = select(Printer).where(
            Printer.is_active == True,
            Printer.status.in_([PrinterStatus.ONLINE, PrinterStatus.PRINTING])
        )
        result = self.db.execute(query)
        return result.scalars().all()
