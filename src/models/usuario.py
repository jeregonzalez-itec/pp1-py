from sqlmodel import Field, SQLModel
from .mascota import Mascota
class UsuarioBase(SQLModel):
    nombre: str
    email: str = Field(
        unique=True
    )  # UNIQUE: Ningún registro va a tener el mismo email que otro.
    activo: bool = Field(default=True)
    mascota_id: int | None = Field(default=None, foreign_key="mascota.id" )


class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    contraseña: str  # Encriptada / Hasheada
    

class UsuarioCreate(UsuarioBase):
    contraseña: str = Field(min_length=6)  # Texto plano


class UsuarioPublic(UsuarioBase):
    id: int


class UsuarioLogin(SQLModel):
    email: str
    contraseña: str