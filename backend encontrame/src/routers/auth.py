from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from core.auth import get_password_hash, jwt_manager, verify_password
from core.dependencies import get_current_user
from core.utils import CONFLICT_RESPONSE, commit_or_409
from database import get_db
from models.usuario import (
    TokenPublic,
    Usuario,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioPublic,
)

auth_routers = APIRouter()


@auth_routers.post(
    "/register",
    response_model=UsuarioPublic,
    status_code=201,
    responses=CONFLICT_RESPONSE,
)
def register(usuario_nuevo: UsuarioCreate, db: Annotated[Session, Depends(get_db)]):
    """Registra un usuario guardando la contraseña hasheada."""
    usuario_db = Usuario.model_validate(usuario_nuevo)
    usuario_db.contraseña = get_password_hash(usuario_nuevo.contraseña)
    db.add(usuario_db)
    commit_or_409(db)
    db.refresh(usuario_db)
    return usuario_db


@auth_routers.post(
    "/login",
    response_model=TokenPublic,
    responses={
        401: {
            "description": "Credenciales incorrectas",
            "content": {
                "application/json": {"example": {"detail": "Email o contraseña incorrectos"}}
            },
        }
    },
)
def login(usuario: UsuarioLogin, db: Annotated[Session, Depends(get_db)]):
    """Valida credenciales y devuelve un JWT."""
    usuario_db = db.exec(select(Usuario).where(Usuario.email == usuario.email)).first()
    if (
        usuario_db is None
        or not usuario_db.activo
        or not verify_password(usuario.contraseña, usuario_db.contraseña)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    token = jwt_manager.create_access_token({"sub": usuario_db.email})
    return TokenPublic(access_token=token)


@auth_routers.get("/me", response_model=UsuarioPublic)
def perfil(usuario: Annotated[Usuario, Depends(get_current_user)]):
    """Ruta protegida: devuelve el usuario dueño del token."""
    return usuario
