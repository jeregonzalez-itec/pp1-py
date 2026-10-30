from typing import TYPE_CHECKING, Annotated, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .tagnfc import TagNFC
    from .usuario import Usuario


class MascotaBase(SQLModel):
    nombre: Annotated[str, Field(max_length=60)]
    especie: Annotated[str, Field(max_length=40)]
    raza: Annotated[str, Field(max_length=60)]
    estado: Annotated[bool, Field(description="True = activa, False = baja lógica")] = True
    # Un tag NFC identifica a una sola mascota (UNIQUE)
    tag_id: int | None = Field(default=None, foreign_key="tagnfc.id", unique=True)
    usuario_id: int | None = Field(default=None, foreign_key="usuario.id")


class Mascota(MascotaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tag: Optional["TagNFC"] = Relationship(back_populates="mascota")
    usuario: Optional["Usuario"] = Relationship(back_populates="mascotas")


class MascotaPublic(MascotaBase):
    id: int
