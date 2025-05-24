"""Endpoints para gestión de impresoras."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from printoptimizer.db.session import get_db
from printoptimizer.models.printer import PrinterStatus
from printoptimizer.schemas.printer import (
    Printer,
    PrinterCreate,
    PrinterList,
    PrinterUpdate,
)
from printoptimizer.services.printer_service import PrinterService

router = APIRouter()


@router.get("/", response_model=PrinterList)
def get_printers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    status: Optional[PrinterStatus] = None,
    db: Session = Depends(get_db),
) -> PrinterList:
    """
    Obtener lista de impresoras.
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar
    - **is_active**: Filtrar por estado activo/inactivo
    - **status**: Filtrar por estado de la impresora
    """
    service = PrinterService(db)
    printers = service.get_all(skip, limit, is_active, status)
    
    # Calcular paginación
    total = len(printers)  # En producción, hacer COUNT en la DB
    pages = (total + limit - 1) // limit
    
    return PrinterList(
        items=[Printer.from_orm_with_computed(p) for p in printers],
        total=total,
        page=(skip // limit) + 1,
        page_size=limit,
        pages=pages,
    )


@router.get("/available", response_model=List[Printer])
def get_available_printers(
    db: Session = Depends(get_db),
) -> List[Printer]:
    """Obtener impresoras disponibles para imprimir."""
    service = PrinterService(db)
    printers = service.get_available_printers()
    return [Printer.from_orm_with_computed(p) for p in printers]


@router.get("/{printer_id}", response_model=Printer)
def get_printer(
    printer_id: int,
    db: Session = Depends(get_db),
) -> Printer:
    """Obtener impresora por ID."""
    service = PrinterService(db)
    printer = service.get_by_id(printer_id)
    
    if not printer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Printer with id {printer_id} not found",
        )
    
    return Printer.from_orm_with_computed(printer)


@router.post("/", response_model=Printer, status_code=status.HTTP_201_CREATED)
def create_printer(
    printer_data: PrinterCreate,
    db: Session = Depends(get_db),
) -> Printer:
    """Crear nueva impresora."""
    service = PrinterService(db)
    printer = service.create(printer_data)
    return Printer.from_orm_with_computed(printer)


@router.put("/{printer_id}", response_model=Printer)
def update_printer(
    printer_id: int,
    printer_data: PrinterUpdate,
    db: Session = Depends(get_db),
) -> Printer:
    """Actualizar impresora existente."""
    service = PrinterService(db)
    printer = service.update(printer_id, printer_data)
    
    if not printer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Printer with id {printer_id} not found",
        )
    
    return Printer.from_orm_with_computed(printer)


@router.delete("/{printer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_printer(
    printer_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Eliminar impresora."""
    service = PrinterService(db)
    
    if not service.delete(printer_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Printer with id {printer_id} not found",
        )
