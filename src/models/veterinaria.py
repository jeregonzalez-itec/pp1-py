
from sqlmodel import Field, Relationship, SQLModel
from .tagnfc import TagNFC


class VeterinariaBase(SQLModel):
    nombre: str = Field(max_length=90)
    telefono: str
    activo: bool = Field(default=True)


class Veterinaria(VeterinariaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tags: list["TagNFC"] = Relationship(back_populates="veterinaria")


class VeterinariaPublic(VeterinariaBase):
    id: int
