from typing import Optional
from sqlmodel import SQLModel, Field
from .schemas import ProveedorBase

class Proveedor(ProveedorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
