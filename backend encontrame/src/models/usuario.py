from typing import TYPE_CHECKING, Annotated

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .mascota import Mascota


class UsuarioBase(SQLModel):
    nombre: Annotated[str, Field(max_length=90)]
    # UNIQUE: ningún registro puede repetir el email
    email: str = Field(unique=True, max_length=120)
    activo: Annotated[bool, Field(description="Baja lógica")] = True


class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    contraseña: str  # Hasheada con bcrypt, nunca en texto plano
    mascotas: list["Mascota"] = Relationship(back_populates="usuario")


class UsuarioCreate(UsuarioBase):
    # bcrypt solo admite hasta 72 bytes
    contraseña: Annotated[str, Field(min_length=6, max_length=72)]  # Texto plano


class UsuarioPublic(UsuarioBase):
    id: int


class UsuarioLogin(SQLModel):
    email: str
    contraseña: str


class TokenPublic(SQLModel):
    access_token: str
    token_type: str = "bearer"
