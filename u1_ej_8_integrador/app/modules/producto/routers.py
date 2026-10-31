from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from typing import List

from app.database import get_session
from . import schemas, services

router = APIRouter(prefix="/productos", tags=["Productos"])


# ---------------------------------------------------------
# ALTA DE PRODUCTO
# Método: POST | Endpoint: /productos | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=schemas.ProductoRead, status_code=status.HTTP_201_CREATED
)
def alta_producto(producto: schemas.ProductoCreate, session=Depends(get_session)):
    return services.crear(producto, session)


# (Extra) LISTAR PRODUCTOS
@router.get(
    "/", response_model=List[schemas.ProductoRead], status_code=status.HTTP_200_OK
)
def listar_productos(skip: int = Query(0, ge=0), limit: int = Query(10, le=50), session=Depends(get_session)):
    return services.obtener_todos(skip, limit, session)


# ---------------------------------------------------------
# DETALLE DE PRODUCTO
# Método: GET | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=schemas.ProductoRead, status_code=status.HTTP_200_OK
)
def detalle_producto(id: int = Path(..., gt=0), session=Depends(get_session)):
    producto = services.obtener_por_id(id, session)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo Total)
# Método: PUT | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}", response_model=schemas.ProductoRead, status_code=status.HTTP_200_OK
)
def actualizar_producto(producto: schemas.ProductoCreate, id: int = Path(..., gt=0), session=Depends(get_session)):
    # Usamos ProductoCreate porque es un reemplazo total (exige todos los campos)
    actualizado = services.actualizar_total(id, producto, session)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# BORRADO LÓGICO
# Método: PUT | Endpoint: /productos/{id}/desactivar | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0), session=Depends(get_session)):
    desactivado = services.desactivar(id, session)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return desactivado


# ---------------------------------------------------------
# CONSULTAR STOCK (Lógica de Negocio)
# Método: GET | Endpoint: /productos/{id}/stock | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/stock",
    response_model=schemas.ProductoStockResponse,
    status_code=status.HTTP_200_OK,
)
@router.get("/{id}/stock", response_model=schemas.ProductoStockResponse)
def consultar_stock(id: int = Path(..., gt=0), session=Depends(get_session)):
    resultado = services.obtener_estado_stock(id, session)  # Llamada al servicio
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return resultado  # El router solo devuelve el resultado
