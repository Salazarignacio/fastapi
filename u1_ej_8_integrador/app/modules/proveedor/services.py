from .schemas import ProveedorRead, ProveedorUpdate, ProveedorCreate
from typing import Optional


db_proveedores: list[ProveedorRead] = []
id_counter = 1

def crear(data: ProveedorCreate) -> ProveedorRead:
    global id_counter
    nuevo = ProveedorRead(id=id_counter, **data.model_dump())
    db_proveedores.append(nuevo)
    id_counter += 1
    return nuevo

def obtener_todos(skip: int = 0, limit: int = 100) -> list[ProveedorRead]:
    return db_proveedores[skip: skip + limit]

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
    return None
