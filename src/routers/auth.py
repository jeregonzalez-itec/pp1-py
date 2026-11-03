from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from core.auth import get_password_hash, jwt_manager, verify_password
from core.utils import CONFLICT_RESPONSE, commit_or_409
from database import get_db
from models.usuario import Usuario, UsuarioCreate, UsuarioLogin, UsuarioPublic

auth_routers = APIRouter()


@auth_routers.post(
    "/register",
    response_model=UsuarioPublic,
    status_code=status.HTTP_201_CREATED,
    responses=CONFLICT_RESPONSE,
)
def register(usuario_nuevo: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario con contraseña hasheada."""
    usuario_db = Usuario.model_validate(usuario_nuevo)
    usuario_db.contraseña = get_password_hash(usuario_nuevo.contraseña)

    db.add(usuario_db)
    commit_or_409(db)
    db.refresh(usuario_db)
    return usuario_db


@auth_routers.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    """Autentica las credenciales de un usuario y devuelve su token JWT."""
    query = select(Usuario).where(Usuario.email == usuario.email)
    usuario_db = db.exec(query).first()

    if not usuario_db or not verify_password(usuario.contraseña, usuario_db.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas (email o contraseña inválidos)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario_db.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo en el sistema",
        )

    token = jwt_manager.create_access_token(
        data={"sub": str(usuario_db.id), "email": usuario_db.email}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": UsuarioPublic.model_validate(usuario_db),
    }
