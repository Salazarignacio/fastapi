from fastapi import FastAPI
from app.modules.producto.routers import router as producto_router
from app.modules.categoria.routers import router as categoria_router
from app.modules.proveedor.routers import router as proveedor_router
from u1_ej_8_integrador.app.database import create_db_and_tables

def create_app() -> FastAPI:
    app = FastAPI(
        title="API Integradora - Unidad 1",
        description="Conceptos: Path, Query, Body, Pydantic, Errores.",
        version="1.0.0"
    )
    
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(proveedor_router)
    
    return app

app = create_app()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
