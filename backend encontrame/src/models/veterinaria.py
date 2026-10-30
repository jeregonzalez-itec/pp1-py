from typing import TYPE_CHECKING, Annotated

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .tagnfc import TagNFC


class VeterinariaBase(SQLModel):
    nombre: Annotated[str, Field(max_length=90, description="Nombre de la veterinaria")]
    telefono: Annotated[str, Field(max_length=30)]
    direccion: Annotated[str, Field(max_length=150)]
    activo: Annotated[bool, Field(description="Baja lógica")] = True


class Veterinaria(VeterinariaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tags: list["TagNFC"] = Relationship(back_populates="veterinaria")


class VeterinariaPublic(VeterinariaBase):
    id: int
