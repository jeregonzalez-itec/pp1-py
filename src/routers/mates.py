from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from database import get_db
from models.mate import Mate
from schemas.mates import MateSchema, MateUpdateSchema

mates_routers = APIRouter()
NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Mate no encontrado",
                }
            }
        },
    },
}


# mates_db = [
#     {
#         "id": 1,
#         "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-26-at-15-43-36-15bb01a41683c6b0fa17798993102248-1024-1024.webp",
#         "nombre": "Mate Imperial",
#         "material": "Cuero",
#         "precio": 25000,
#         "stock": 5
#     },
#     {
#         "id": 2,
#         "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-26-at-15-43-43-80291fa244c7918b1717798986879104-1024-1024.webp",
#         "nombre": "Mate Camionero",
#         "material": "Calabaza",
#         "precio": 18000,
#         "stock": 10
#     },
#     {
#         "id": 3,
#         "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-12-at-14-38-58-1-f46bd7a41c5701bff617786537846413-1024-1024.webp",
#         "nombre": "IMPERIAL CRIOLLO DE CALABAZA",
#         "material": "Calabaza",
#         "precio": 40000,
#         "stock": 3
#     },
#     {
#         "id": 4,
#         "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-26-at-15-43-35-3-abf4f884bb4d17e11817798221302116-1024-1024.webp",
#         "nombre": "Mate galleta",
#         "material": "Calabaza",
#         "precio": 20000,
#         "stock": 6
#     },
#     {
#         "id": 5,
#         "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/metalico-87d5ab8228c9808e4717779946991298-1024-1024.webp",
#         "nombre": "Mate Termico",
#         "material": "Acero Inoxidable",
#         "precio": 10000,
#         "stock": 9
#     },
# ] 

mates_db = []

@mates_routers.get("/", response_model=list[MateSchema])
async def get_mates(db: Session = Depends(get_db)):  # Inyección de Dependencias
    # EN SQL SERÍA: SELECT * FROM mates
    mates = db.query(Mate).all()
    return mates


# get by id
@mates_routers.get(
    "/{id}",  # Parámetro de ruta (esta en la url)
    responses=NOT_FOUND_RESPONSE,
    response_model=MateSchema,
)
async def get_mates_by_id(
    id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):

    # mate_obtenido = db.query(Mate).filter(Mate.id == id).first()
    # SELECT * FROM mates WHERE mate_id = 6

    mate_obtenido = db.get(Mate, id)
    if mate_obtenido is not None:
        return mate_obtenido
    raise HTTPException(status_code=404, detail="Mate no encontrado")


@mates_routers.post("/", response_model=MateSchema)  # VALIDO EL DATO DE SALIDA
async def crear_mate(
    mate_nuevo: MateSchema, db: Session = Depends(get_db)
):  # VALIDO EL DATO DE ENTRADA

    mate_db = Mate(  # <- MODELO
        nombre=mate_nuevo.nombre,
        precio=mate_nuevo.precio,
        stock=mate_nuevo.stock,
        material=mate_nuevo.material,
        descripcion=mate_nuevo.descripcion,
        disponible=mate_nuevo.disponible
    )
    # Un objeto de un Model, equivale a un registro en una Tabla
    db.add(mate_db)
    # persistimos en la db con commit
    db.commit()
    # refrescamos UNA INSTANCIA (objeto)
    db.refresh(mate_db)
    return mate_db


@mates_routers.put(
    "/{id}", responses=NOT_FOUND_RESPONSE, response_model=MateSchema 
)
async def editar_mate(
    id: Annotated[int, Path(gt=0, description="Id del producto. >0")],
    # ^^ El tipo puede ser modularizado, no?
    mate_editar: MateUpdateSchema,
    db: Session = Depends(get_db),
):

    mate_obtenido = db.get(Mate, id)
    if mate_obtenido is not None:
        mate_obtenido.nombre = mate_editar.nombre
        mate_obtenido.precio = mate_editar.precio
        mate_obtenido.stock = mate_editar.stock
        mate_obtenido.material = mate_editar.material
        mate_obtenido.descripcion = mate_editar.descripcion
        mate_obtenido.disponible = mate_editar.disponible
        db.commit()
        db.refresh(mate_obtenido)
        return mate_obtenido

    raise HTTPException(status_code=404, detail="Mate no encontrado")


@mates_routers.delete(
    "/{id}",  # ?logico=false
    responses=NOT_FOUND_RESPONSE,  # DOCUMENTACION
    response_model=list[MateSchema],  # VALIDACION DATOS DE SALIDA
)
async def borrar_mate(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
) -> MateSchema:

    mate_obtenido = db.get(Mate, id)
    if mate_obtenido is not None:
        if logico:
            mate_obtenido.disponible = False
        else:
            db.delete(mate_obtenido)
            db.commit()
        return db.query(Mate).all()
    raise HTTPException(status_code=404, detail="Mate no encontrado")