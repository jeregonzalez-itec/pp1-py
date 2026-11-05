from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from core.utils import CONFLICT_RESPONSE, commit_or_409, get_or_404, not_found_response
from database import get_db
from models.anidados import TagNFCNested
from models.tagnfc import TagNFC, TagNFCBase, TagNFCPublic
from models.veterinaria import Veterinaria

tagnfc_routers = APIRouter()
LABEL = "Tag NFC"
NOT_FOUND_RESPONSE = not_found_response(LABEL)


@tagnfc_routers.get("/", response_model=Page[TagNFCPublic])
def listar_tags(db: Annotated[Session, Depends(get_db)]):
    """Lista paginada de tags NFC (?page=1&size=50)."""
    return paginate(db, select(TagNFC))


@tagnfc_routers.get("/{id}", response_model=TagNFCNested, responses=NOT_FOUND_RESPONSE)
def obtener_tag(
    id: Annotated[int, Path(gt=0, description="Id del tag. >0")],
    db: Annotated[Session, Depends(get_db)],
):
    """Devuelve un tag con su veterinaria y su mascota anidadas."""
    return get_or_404(db, TagNFC, id, LABEL)


@tagnfc_routers.post(
    "/",
    response_model=TagNFCPublic,
    status_code=201,
    responses={**not_found_response("Veterinaria"), **CONFLICT_RESPONSE},
)
def crear_tag(tag: TagNFCBase, db: Annotated[Session, Depends(get_db)]):
    if tag.veterinaria_id is not None:
        get_or_404(db, Veterinaria, tag.veterinaria_id, "Veterinaria")
    nuevo = TagNFC.model_validate(tag)
    db.add(nuevo)
    commit_or_409(db)
    db.refresh(nuevo)
    return nuevo


@tagnfc_routers.put(
    "/{id}",
    response_model=TagNFCPublic,
    responses={**NOT_FOUND_RESPONSE, **CONFLICT_RESPONSE},
)
def editar_tag(
    id: Annotated[int, Path(gt=0)],
    tag_editar: TagNFCBase,
    db: Annotated[Session, Depends(get_db)],
):
    obtenido = get_or_404(db, TagNFC, id, LABEL)
    if tag_editar.veterinaria_id is not None:
        get_or_404(db, Veterinaria, tag_editar.veterinaria_id, "Veterinaria")
    obtenido.sqlmodel_update(tag_editar.model_dump())
    db.add(obtenido)
    commit_or_409(db)
    db.refresh(obtenido)
    return obtenido


@tagnfc_routers.delete(
    "/{id}",
    response_model=TagNFCPublic,
    responses={**NOT_FOUND_RESPONSE, **CONFLICT_RESPONSE},
)
def borrar_tag(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="True = baja lógica (mantiene el registro)")] = False,
):
    obtenido = get_or_404(db, TagNFC, id, LABEL)
    if logico:
        obtenido.activo = False
        db.add(obtenido)
        commit_or_409(db)
        db.refresh(obtenido)
        return obtenido
    if obtenido.mascota:
        raise HTTPException(
            status_code=409,
            detail="El tag está asignado a una mascota; usá ?logico=true",
        )
    eliminado = TagNFCPublic.model_validate(obtenido)
    db.delete(obtenido)
    commit_or_409(db)
    return eliminado
