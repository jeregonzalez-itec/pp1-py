from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi_pagination import Page, paginate
from sqlmodel import Session, select
from database import get_db
from models.mate import Mate,MateBase,MatePublic
from models.anidados import MateNested
mates_routers = APIRouter()
NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Artículo no encontrado",
                }
            }
        },
    },
}


@mates_routers.get(
        "/", response_model=Page[MatePublic]
)
async def get_mates(db: Session = Depends(get_db)):  # Inyección de Dependencias
    # EN SQL SERÍA: SELECT * FROM mates
    mates = db.exec(select(Mate)).all()
    return mates


# get by id
@mates_routers.get(
    "/{id}",  # Parámetro de ruta (esta en la url)
    responses=NOT_FOUND_RESPONSE,
    response_model=MateNested,
)

async def get_mates_by_id(
    id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):

    mate_obtenido = db.get(Mate, id)
    if mate_obtenido is not None:
        return mate_obtenido
    raise HTTPException(status_code=404, detail="Mate no encontrado")


@mates_routers.post("/", response_model=MatePublic)  # VALIDO EL DATO DE SALIDA
async def crear_mate(
    mate_nuevo: MatePublic, db: Session = Depends(get_db)
):  # VALIDO EL DATO DE ENTRADA

    mate_db = Mate.model_validate(mate_nuevo)
    # Un objeto de un Model, equivale a un registro en una Tabla
    db.add(mate_db)
    # persistimos en la db con commit
    db.commit()
    # refrescamos UNA INSTANCIA (objeto)
    db.refresh(mate_db)
    return mate_db


@mates_routers.put(
    "/{id}", responses=NOT_FOUND_RESPONSE, response_model=MatePublic 
)
async def editar_mate(
    id: Annotated[int, Path(gt=0, description="Id del producto. >0")],
    # ^^ El tipo puede ser modularizado, no?
    mate_editar: MateBase,
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
    response_model=MatePublic,  # VALIDACION DATOS DE SALIDA
)
async def borrar_mate(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
) -> MatePublic:

    mate_obtenido = db.get(Mate, id)
    if mate_obtenido is not None:
        if logico:
            mate_obtenido.disponible = False
        else:
            db.delete(mate_obtenido)
            db.commit()
        return db.exec(select(Mate)).all()
    raise HTTPException(status_code=404, detail="Mate no encontrado")