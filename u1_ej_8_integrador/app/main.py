from fastapi import FastAPI
from app.modules.producto.routers import router as producto_router
from app.modules.categoria.routers import router as categoria_router
from app.modules.proveedor.routers import router as proveedor_router
from app.database import create_db_and_tables

def create_app() -> FastAPI:
    app = FastAPI(
        title="API Integradora - Unidad 1",
        description="Conceptos: Path, Query, Body, Pydantic, Errores.",
        version="1.0.0"
    )
    
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(proveedor_router)
    create_db_and_tables()
    return app

app = create_app()

"""1) En categoria/routers.py importás Session desde la librería requests (HTTP) en vez de sqlmodel, 
un error de tipeo que muestra que el código no se probó con cuidado. 

2) La validación de nombre/código duplicado, que implementaste en los tres módulos, no funciona en ninguno: 
en producto, crear devuelve None en vez de levantar una excepción (el except ValueError del router nunca 
se dispara); en categoría no hay ningún chequeo de duplicados; y en proveedor, existe_codigo sigue 
comparando contra una lista en memoria que nunca se llena (db_proveedores = []) y encima el router le 
pasa la sesión de base de datos en el parámetro que espera un ID a excluir. 

3) Quedan restos de código de una versión anterior sin base de datos (db_categorias, db_proveedores, id_counter) 
que ya no se usan y conviene borrar """