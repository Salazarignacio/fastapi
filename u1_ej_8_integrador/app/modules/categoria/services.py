from typing import List, Optional

from sqlmodel import Session, select

from .models import Categoria
from .schemas import CategoriaCreate, CategoriaRead

# Simulamos algunos registros iniciales
db_categorias: List[CategoriaRead] = [
    CategoriaRead(id=1, codigo="MUE-01", descripcion="Muebles de Oficina", activo=True),
    CategoriaRead(id=2, codigo="ELE-02", descripcion="Electrónica", activo=True),
]
id_counter = 3


def crear(data: CategoriaCreate, session: Session) -> CategoriaRead:
    
    nueva = Categoria(**data.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


def obtener_todas(skip: int = 0, limit: int = 10, session: Session = None) -> List[CategoriaRead]:
    categorias = select(Categoria)
    result = session.exec(categorias.offset(skip).limit(limit))
    return result.all()


def obtener_por_id(id: int, session: Session) -> Optional[CategoriaRead]:
    categoria = session.get(Categoria, id)
    if categoria is None:
        raise ValueError("Categoría no encontrada")
    return categoria


def actualizar_total(id: int, data: CategoriaCreate, session: Session) -> Optional[CategoriaRead]:
    categoria = session.get(Categoria, id)
    for field, value in data.model_dump().items():
        setattr(categoria, field, value)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

def desactivar(id: int, session: Session) -> Optional[CategoriaRead]:
    categoria = session.get(Categoria, id)
    categoria.activo = False
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
    return None
