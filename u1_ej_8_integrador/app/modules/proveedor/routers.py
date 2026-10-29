from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from . import schemas, services
from app.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.post(
    "/", response_model=schemas.ProveedorRead, status_code=status.HTTP_201_CREATED
)
def alta_proveedor(proveedor: schemas.ProveedorCreate, session: Session = Depends(get_session)):
    if services.existe_codigo(proveedor.codigo, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un proveedor con el código {proveedor.codigo}",
        )
    return services.crear(proveedor, session)


@router.get(
    "/", response_model=List[schemas.ProveedorRead], status_code=status.HTTP_200_OK
)
def listar_proveedores(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50), activo: bool | None = Query(None), session: Session = Depends(get_session)):
    return services.obtener_todos(skip, limit, activo, session)


@router.get(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def obtener_proveedor(id: int = Path(..., gt=0)):
    proveedor = services.obtener_por_id(id)
    if proveedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    return proveedor

@router.put(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def actualizar_proveedor(proveedor: schemas.ProveedorCreate, id: int = Path(..., gt=0)):
    if services.obtener_por_id(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    if services.existe_codigo(proveedor.codigo, excluir_id=id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un proveedor con el código {proveedor.codigo}",
        )
    return services.actualizar_total(id, proveedor)

@router.put("/{id}/desactivar", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK)
def borrado_logico(id: int = Path(..., gt=0)):
    proveedor = services.obtener_por_id(id)
    if proveedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    if not proveedor.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proveedor ya está desactivado",
        )
    return services.desactivar(id)
