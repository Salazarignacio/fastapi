from typing import Optional
from sqlmodel import SQLModel, Field

class ProveedorBase(SQLModel):
    codigo: str = Field(min_length=1)
    razon_social: str = Field(min_length=3)
    cuit: str = Field(min_length=11, max_length=15)
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: bool = True

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorRead(ProveedorBase, table=True):
    id: int

class ProveedorUpdate(ProveedorBase):
    codigo: Optional[str] = None
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None