from typing import Optional
from sqlmodel import Field
from .schemas import CategoriaBase


class Categoria(CategoriaBase, table=True):
     id: Optional[int] = Field(default=None, primary_key=True)