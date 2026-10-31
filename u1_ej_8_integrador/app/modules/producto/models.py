from typing import Optional
from sqlmodel import Field
from .schemas import ProductoBase

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)