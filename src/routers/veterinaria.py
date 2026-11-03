from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from core.utils import CONFLICT_RESPONSE, commit_or_409, get_or_404, not_found_response
from database import get_db
from models.anidados import VeterinariaNested
from models.veterinaria import Veterinaria, VeterinariaBase, VeterinariaPublic

veterinaria_routers = APIRouter()
LABEL = "Veterinaria"
NOT_FOUND_RESPONSE = not_found_response(LABEL)


@veterinaria_routers.get("/", response_model=Page[VeterinariaPublic])
def listar_veterinarias(db: Annotated[Session, Depends(get_db)]):
    """Lista paginada de veterinarias (?page=1&size=50)."""
    return paginate(db, select(Veterinaria))


@veterinaria_routers.get(
    "/{id}", response_model=VeterinariaNested, responses=NOT_FOUND_RESPONSE
)
def obtener_veterinaria(
    id: Annotated[int, Path(gt=0, description="Id de la veterinaria. >0")],
    db: Annotated[Session, Depends(get_db)],
):
    """Devuelve una veterinaria con sus tags NFC anidados."""
    return get_or_404(db, Veterinaria, id, LABEL)


@veterinaria_routers.post("/", response_model=VeterinariaPublic, status_code=201)
def crear_veterinaria(
    veterinaria: VeterinariaBase, db: Annotated[Session, Depends(get_db)]
):
    nueva = Veterinaria.model_validate(veterinaria)
    db.add(nueva)
    commit_or_409(db)
    db.refresh(nueva)
    return nueva


@veterinaria_routers.put(
    "/{id}", response_model=VeterinariaPublic, responses=NOT_FOUND_RESPONSE
)
def editar_veterinaria(
    id: Annotated[int, Path(gt=0)],
    veterinaria_editar: VeterinariaBase,
    db: Annotated[Session, Depends(get_db)],
):
    obtenida = get_or_404(db, Veterinaria, id, LABEL)
    obtenida.sqlmodel_update(veterinaria_editar.model_dump())
    db.add(obtenida)
    commit_or_409(db)
    db.refresh(obtenida)
    return obtenida


@veterinaria_routers.delete(
    "/{id}",
    response_model=VeterinariaPublic,
    responses={**NOT_FOUND_RESPONSE, **CONFLICT_RESPONSE},
)
def borrar_veterinaria(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="True = baja lógica (mantiene el registro)")] = False,
):
    obtenida = get_or_404(db, Veterinaria, id, LABEL)
    if logico:
        obtenida.activo = False
        db.add(obtenida)
        commit_or_409(db)
        db.refresh(obtenida)
        return obtenida
    if obtenida.tags:
        raise HTTPException(
            status_code=409,
            detail="La veterinaria tiene tags asociados; usá ?logico=true",
        )
    eliminada = VeterinariaPublic.model_validate(obtenida)
    db.delete(obtenida)
    commit_or_409(db)
    return eliminada
