from sqlmodel import Session, select
from .schemas import ProveedorRead, ProveedorUpdate, ProveedorCreate
from typing import Optional
from app.database import get_session
from .models import Proveedor

def crear(data: ProveedorCreate, session: Session) -> ProveedorRead:
    nuevo = Proveedor(**data.model_dump())
    if obtener_por_codigo(data.codigo, session):
        raise ValueError("Ya existe un proveedor con ese código")
    session.add(nuevo)  
    session.commit()
    session.refresh(nuevo)

    return nuevo

def obtener_por_codigo(codigo: str, session: Session) -> Optional[ProveedorRead]:
    proveedor = select(Proveedor).where(Proveedor.codigo == codigo)
    return session.exec(proveedor).first()


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
    proveedor = obtener_por_id(id, session)
    if obtener_por_codigo(data.codigo, session):
        raise ValueError("Ya existe un proveedor con ese código")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(proveedor, field, value)

    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor
    
def desactivar(id: int, session: Session) -> Optional[ProveedorRead]:
    proveedor = obtener_por_id(id, session)
    proveedor.activo = False
    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor
