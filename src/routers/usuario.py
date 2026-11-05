from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from core.auth import get_password_hash
from core.utils import CONFLICT_RESPONSE, commit_or_409, get_or_404, not_found_response
from database import get_db
from models.anidados import UsuarioNested
from models.usuario import Usuario, UsuarioBase, UsuarioCreate, UsuarioPublic

usuario_routers = APIRouter()
LABEL = "Usuario"
NOT_FOUND_RESPONSE = not_found_response(LABEL)


@usuario_routers.get("/", response_model=Page[UsuarioPublic])
def listar_usuarios(db: Annotated[Session, Depends(get_db)]):
    """Lista paginada de usuarios (?page=1&size=50)."""
    return paginate(db, select(Usuario))


@usuario_routers.get("/{id}", response_model=UsuarioNested, responses=NOT_FOUND_RESPONSE)
def obtener_usuario(
    id: Annotated[int, Path(gt=0, description="Id del usuario. >0")],
    db: Annotated[Session, Depends(get_db)],
):
    """Devuelve un usuario con sus mascotas anidadas."""
    return get_or_404(db, Usuario, id, LABEL)


@usuario_routers.post(
    "/", response_model=UsuarioPublic, status_code=201, responses=CONFLICT_RESPONSE
)
def crear_usuario(usuario: UsuarioCreate, db: Annotated[Session, Depends(get_db)]):
    nuevo = Usuario.model_validate(usuario)
    nuevo.contraseña = get_password_hash(usuario.contraseña)
    db.add(nuevo)
    commit_or_409(db)
    db.refresh(nuevo)
    return nuevo


@usuario_routers.put(
    "/{id}",
    response_model=UsuarioPublic,
    responses={**NOT_FOUND_RESPONSE, **CONFLICT_RESPONSE},
)
def editar_usuario(
    id: Annotated[int, Path(gt=0)],
    usuario_editar: UsuarioBase,
    db: Annotated[Session, Depends(get_db)],
):
    """Edita nombre, email y estado. La contraseña no se modifica acá."""
    obtenido = get_or_404(db, Usuario, id, LABEL)
    obtenido.sqlmodel_update(usuario_editar.model_dump())
    db.add(obtenido)
    commit_or_409(db)
    db.refresh(obtenido)
    return obtenido


@usuario_routers.delete(
    "/{id}",
    response_model=UsuarioPublic,
    responses={**NOT_FOUND_RESPONSE, **CONFLICT_RESPONSE},
)
def borrar_usuario(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="True = baja lógica (mantiene el registro)")] = False,
):
    obtenido = get_or_404(db, Usuario, id, LABEL)
    if logico:
        obtenido.activo = False
        db.add(obtenido)
        commit_or_409(db)
        db.refresh(obtenido)
        return obtenido
    if obtenido.mascotas:
        raise HTTPException(
            status_code=409,
            detail="El usuario tiene mascotas asociadas; usá ?logico=true",
        )
    eliminado = UsuarioPublic.model_validate(obtenido)
    db.delete(obtenido)
    commit_or_409(db)
    return eliminado
