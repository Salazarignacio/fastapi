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

def obtener_por_id(id: int) -> ProveedorRead | None:
    for p in db_proveedores:
        if p.id == id:
            return p
    return None

def actualizar_total(id: int, data: ProveedorRead) -> Optional[ProveedorRead]:

    for index, p in enumerate(db_proveedores):
        if p.id == id:
            proveedor_actualizado = ProveedorRead(id=id, **data.model_dump(exclude={'id'}))
            db_proveedores[index] = proveedor_actualizado
            return proveedor_actualizado
    return None

def desactivar(id: int) -> Optional[ProveedorRead]:
    for index, p in enumerate(db_proveedores):
        if p.id == id:
            p_dict = p.model_dump()
            p_dict["activo"] = False
            proveedor_actualizado = ProveedorRead(**p_dict)
            db_proveedores[index] = proveedor_actualizado
            return proveedor_actualizado
        else:
            raise ValueError(f"Proveedor con id {id} no encontrado o ya desactivado")
    return None
