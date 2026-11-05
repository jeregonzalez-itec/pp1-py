from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

from .estadoMascota import RolUsuarioEnum

if TYPE_CHECKING:
    from .mascota import Mascota


class UsuarioBase(SQLModel):
    nombre: str
    email: str = Field(unique=True, index=True)
    telefono: Optional[str] = Field(default=None, description="Número de teléfono principal para contacto/WhatsApp")
    telefono_secundario: Optional[str] = Field(default=None, description="Número de emergencia adicional")
    direccion: Optional[str] = Field(default=None)
    ciudad: Optional[str] = Field(default=None)
    rol: str = Field(default=RolUsuarioEnum.DUENO)
    activo: bool = Field(default=True)


class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    contraseña: str  # Hash encriptado

    mascotas: list["Mascota"] = Relationship(back_populates="usuario")


class UsuarioCreate(UsuarioBase):
    contraseña: str = Field(min_length=6)


class UsuarioPublic(UsuarioBase):
    id: int


class UsuarioLogin(SQLModel):
    email: str
    contraseña: str
