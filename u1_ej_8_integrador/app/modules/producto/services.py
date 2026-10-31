from typing import List, Optional

from sqlmodel import Session, select
from .models import Producto
from .schemas import ProductoCreate, ProductoRead

# Simulamos que la BD guarda objetos tipo ProductoRead (con ID asignado)
db_productos: List[ProductoRead] = []
id_counter = 1


def crear(data: ProductoCreate, session: Session) -> ProductoRead:
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def obtener_todos(skip: int, limit: int, session: Session) -> List[ProductoRead]:
    query = select(Producto)
    return session.exec(query.offset(skip).limit(limit)).all()


def obtener_por_id(id: int, session: Session) -> Optional[ProductoRead]:
    producto = session.get(Producto, id)
    if producto is None:
        raise ValueError("Producto no encontrado")
    return producto

def actualizar_total(id: int, data: ProductoCreate, session: Session) -> Optional[ProductoRead]:
    producto = obtener_por_id(id, session)  
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
    producto.activo = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def obtener_estado_stock(id: int, session: Session) -> Optional[dict]:
    producto = obtener_por_id(id, session)

    # La lógica de negocio vive aquí
    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo,
    }
