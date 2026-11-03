from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from core.utils import CONFLICT_RESPONSE, commit_or_409, get_or_404, not_found_response
from database import get_db
from models.anidados import MascotaNested
from models.mascota import Mascota, MascotaBase, MascotaPublic
from models.tagnfc import TagNFC
from models.usuario import Usuario

mascota_routers = APIRouter()
LABEL = "Mascota"
NOT_FOUND_RESPONSE = not_found_response(LABEL)


def _validar_relaciones(db: Session, datos: MascotaBase) -> None:
    """Verifica que el tag y el usuario referenciados existan (404 si no)."""
    if datos.tag_id is not None:
        get_or_404(db, TagNFC, datos.tag_id, "Tag NFC")
    if datos.usuario_id is not None:
        get_or_404(db, Usuario, datos.usuario_id, "Usuario")


@mascota_routers.get("/", response_model=Page[MascotaPublic])
def listar_mascotas(db: Annotated[Session, Depends(get_db)]):
    """Lista paginada de mascotas (?page=1&size=50)."""
    return paginate(db, select(Mascota))


@mascota_routers.get("/{id}", response_model=MascotaNested, responses=NOT_FOUND_RESPONSE)
def obtener_mascota(
    id: Annotated[int, Path(gt=0, description="Id de la mascota. >0")],
    db: Annotated[Session, Depends(get_db)],
):
    """Devuelve una mascota con su tag NFC y su dueño anidados."""
    return get_or_404(db, Mascota, id, LABEL)


@mascota_routers.post(
    "/",
    response_model=MascotaPublic,
    status_code=201,
    responses={**not_found_response("Tag NFC / Usuario"), **CONFLICT_RESPONSE},
)
def crear_mascota(mascota: MascotaBase, db: Annotated[Session, Depends(get_db)]):
    _validar_relaciones(db, mascota)
    nueva = Mascota.model_validate(mascota)
    db.add(nueva)
    commit_or_409(db)
    db.refresh(nueva)
    return nueva


@mascota_routers.put(
    "/{id}",
    response_model=MascotaPublic,
    responses={**NOT_FOUND_RESPONSE, **CONFLICT_RESPONSE},
)
def editar_mascota(
    id: Annotated[int, Path(gt=0)],
    mascota_editar: MascotaBase,
    db: Annotated[Session, Depends(get_db)],
):
    obtenida = get_or_404(db, Mascota, id, LABEL)
    _validar_relaciones(db, mascota_editar)
    obtenida.sqlmodel_update(mascota_editar.model_dump())
    db.add(obtenida)
    commit_or_409(db)
    db.refresh(obtenida)
    return obtenida


@mascota_routers.delete(
    "/{id}", response_model=MascotaPublic, responses=NOT_FOUND_RESPONSE
)
def borrar_mascota(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="True = baja lógica (mantiene el registro)")] = False,
):
    obtenida = get_or_404(db, Mascota, id, LABEL)
    if logico:
        obtenida.estado = False
        db.add(obtenida)
        commit_or_409(db)
        db.refresh(obtenida)
        return obtenida
    eliminada = MascotaPublic.model_validate(obtenida)
    db.delete(obtenida)
    commit_or_409(db)
    return eliminada
