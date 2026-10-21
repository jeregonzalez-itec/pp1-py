from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from database import get_db
from models.anidados import ProveedorNested
from models.veterinaria import Proveedor, ProveedorBase, ProveedorPublic
proveedor_routers = APIRouter()
NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Proveedor no encontrado",
                }
            }
        },
    },
}

@proveedor_routers.get("/", response_model=list[ProveedorNested])
async def get_(db: Session = Depends(get_db)):  # Inyección de Dependencias
    articulos = db.exec(select(Proveedor)).all()
    return articulos


@proveedor_routers.post(
    "/", response_model=ProveedorPublic
)  # parametro query -> endpoint?clave=valor&otra_clave=valor
async def crear_proveedor(proveedor: ProveedorBase, db: Session = Depends(get_db)):
    # proveedors
    nuevo_prove = Proveedor.model_validate(proveedor)

    db.add(nuevo_prove)
    db.commit()
    db.refresh(nuevo_prove)
    return nuevo_prove

@proveedor_routers.put(
    "/{id}", responses=NOT_FOUND_RESPONSE, response_model=ProveedorPublic 
)
async def editar_proveedor(
    id: Annotated[int, Path(gt=0, description="Id del proveedor. >0")],
    # ^^ El tipo puede ser modularizado, no?
    proveedor_editar: ProveedorBase,
    db: Session = Depends(get_db),
):

    proveedor_obtenido = db.get(Proveedor, id)
    if proveedor_obtenido is not None:
        proveedor_obtenido.nombre = proveedor_editar.nombre
        proveedor_obtenido.telefono = proveedor_editar.telefono
        db.commit()
        db.refresh(proveedor_obtenido)
        return proveedor_obtenido

    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


@proveedor_routers.delete(
    "/{id}",  # ?logico=false
    responses=NOT_FOUND_RESPONSE,  # DOCUMENTACION
    response_model=list[ProveedorPublic],  # VALIDACION DATOS DE SALIDA
)
async def borrar_proveedor(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
) -> ProveedorPublic:

    proveedor_obtenido = db.get(Proveedor, id)
    if proveedor_obtenido is not None:
        if logico:
            proveedor_obtenido.disponible = False
        else:
            db.delete(proveedor_obtenido)
            db.commit()
        return db.exec(select(Proveedor)).all()
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")