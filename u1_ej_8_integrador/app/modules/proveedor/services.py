from sqlmodel import Session, select
from .schemas import ProveedorRead, ProveedorUpdate, ProveedorCreate
from typing import Optional
from app.database import get_session
from .models import Proveedor



db_proveedores: list[ProveedorRead] = []
id_counter = 1

def crear(data: ProveedorCreate, session: Session) -> ProveedorRead:
    nuevo = Proveedor(**data.model_dump())
    session.add(nuevo)  
    session.commit()
    session.refresh(nuevo)

    return nuevo

def existe_codigo(codigo: str, excluir_id: int | None = None) -> bool:
    return any(p.codigo == codigo and p.id != excluir_id for p in db_proveedores)

def obtener_todos(skip: int, limit: int, activo: bool | None, session: Session) -> list[ProveedorRead]:
    proveedores_elegidos = select(Proveedor)
    if activo is not None:
        proveedores_elegidos = proveedores_elegidos.where(Proveedor.activo == activo)
    proveedores_elegidos = proveedores_elegidos.offset(skip).limit(limit)
    result = session.exec(proveedores_elegidos)

    return result.all()

def obtener_por_id(id: int, session: Session) -> ProveedorRead | None:
    hero = session.get(Proveedor, id)   
    if hero is None:
        return None
    return hero

def actualizar_total(id: int, data: ProveedorRead, session : Session) -> Optional[ProveedorRead]:
    proveedor = session.get(Proveedor, id)
    if proveedor is None:
        raise ValueError("Proveedor no encontrado")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(proveedor, field, value)

    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor
    
def desactivar(id: int, session: Session) -> Optional[ProveedorRead]:
    proveedor = session.get(Proveedor, id)
    if proveedor is None:
        raise ValueError("Proveedor no encontrado")
    if not proveedor.activo:
        raise ValueError("El proveedor ya está desactivado")
    proveedor.activo = False
    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor
