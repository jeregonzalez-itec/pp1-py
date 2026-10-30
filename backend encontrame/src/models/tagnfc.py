from typing import TYPE_CHECKING, Annotated, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .mascota import Mascota
    from .veterinaria import Veterinaria


class TagNFCBase(SQLModel):
    codigo_qr: str = Field(unique=True, max_length=60)
    uid_nfc: str = Field(unique=True, max_length=60)
    precio: Annotated[int, Field(ge=0, description="Precio en pesos")]
    activo: Annotated[bool, Field(description="Baja lógica")] = True
    veterinaria_id: int | None = Field(default=None, foreign_key="veterinaria.id")


class TagNFC(TagNFCBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    veterinaria: Optional["Veterinaria"] = Relationship(back_populates="tags")
    mascota: Optional["Mascota"] = Relationship(back_populates="tag")


class TagNFCPublic(TagNFCBase):
    id: int
