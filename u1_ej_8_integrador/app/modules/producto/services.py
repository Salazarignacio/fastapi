from typing import List, Optional

from sqlmodel import Session, select
from .models import Producto
from .schemas import ProductoCreate, ProductoRead


def crear(data: ProductoCreate, session: Session) -> ProductoRead:
    nuevo = Producto(**data.model_dump())
    producto = select(Producto).where(Producto.nombre == data.nombre)
    if session.exec(producto).first():
        raise ValueError("Producto ya existe")
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def obtener_todos(skip: int, limit: int, session: Session) -> List[ProductoRead]:
    query = select(Producto)
    return session.exec(query.offset(skip).limit(limit)).all()


def obtener_por_id(id: int, session: Session) -> Optional[ProductoRead]:
    producto = session.get(Producto, id)
    return producto

def actualizar_total(id: int, data: ProductoCreate, session: Session) -> Optional[ProductoRead]:
    producto = obtener_por_id(id, session)  
    if producto is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(producto, field, value)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def desactivar(id: int, session: Session) -> Optional[ProductoRead]:
    # Borrado lógico: Solo altera el estado 'activo'
    producto = obtener_por_id(id, session)
    if producto is None:
        return None
    producto.activo = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def obtener_estado_stock(id: int, session: Session) -> Optional[dict]:
    producto = obtener_por_id(id, session)
    if producto is None:
        return None

    # La lógica de negocio vive aquí
    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo,
    }
