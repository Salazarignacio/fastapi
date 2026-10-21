from pydantic import BaseModel, Field
from typing import Optional


class ProveedorBase(BaseModel):
    codigo: str = Field(min_length=1)
    razon_social: str = Field(min_length=3)
    cuit: str = Field(min_length=11, max_length=15)
    email: str | None = None
    telefono: str | None = None
    activo: bool = True


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorRead(ProveedorBase):
    id: int


class ProveedorUpdate(BaseModel):
    codigo: Optional[str] | None = None
    razon_social: Optional[str] | None = None
    cuit: Optional[str] | None = None
    email: Optional[str] | None = None
    telefono: Optional[str] | None = None
    activo: Optional[bool] | None = None
