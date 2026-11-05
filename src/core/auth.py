from datetime import datetime, timedelta, timezone
import os
from typing import Optional
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session

from database import get_db
from models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    """
    Función que a partir de una contraseña en texto plano, genera un hash.
    Convierte el str plano en bytes, genera un salt único y la 'encripta'.
    Devuelve el hash creado a partir de la contraseña. Es lo hay que guardar en la DB.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()  # Identificador único para generar el hash
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")
    return hashed_pwd


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Chequea si la contraseña en texto plano coincide con la contraseña hasheada.
    No se 'des-encripta', devuelve True o False.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 60 * 24 * 7):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, data: dict) -> str:
        """
        Crea un token JWT firmado.
        'data' debe contener al menos el 'sub' (subject), que suele ser el ID del usuario.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        """
        Decodifica el token. Si algo falla, interrumpe la petición con un error HTTP 401.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token ha expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )


jwt_manager = JWTManager(
    secret_key=os.getenv("SECRET_KEY", "clave_super_secreta_development_encontrame_2026"),
    expire_minutes=60 * 24 * 7,  # 7 días para comodidad en móviles
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """Dependencia para obtener el usuario autenticado a partir del token JWT."""
    payload = jwt_manager.verify_token(token)
    user_id_raw = payload.get("sub")
    if not user_id_raw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no contiene identificación válida",
        )
    try:
        user_id = int(user_id_raw)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identificador de usuario inválido en token",
        )

    usuario = db.get(Usuario, user_id)
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o dado de baja",
        )
    return usuario
