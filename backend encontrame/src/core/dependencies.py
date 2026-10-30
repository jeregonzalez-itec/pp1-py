from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from core.auth import jwt_manager
from database import get_db
from models.usuario import Usuario

# Esquema "Bearer": habilita el botón Authorize en /docs
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Usuario:
    """Devuelve el usuario dueño del token JWT (o 401 si no es válido)."""
    payload = jwt_manager.verify_token(credentials.credentials)
    email = payload.get("sub")
    usuario = db.exec(select(Usuario).where(Usuario.email == email)).first()
    if usuario is None or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inválido o inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario
