from sqlmodel import Field, SQLModel, Relationship
from .veterinaria import Veterinaria
class TagNFCBase(SQLModel):
    codigoQR: str
    uidNFC: str
    precio: int
    activo: bool
    veterinaria_id: int | None = Field(default=None, foreign_key="veterinaria.id" )


class TagNFC(TagNFCBase,table = True):
       id: int | None = Field(default=None, primary_key=True)
       veterinaria: Veterinaria | None = Relationship(back_populates="tagnfc")

class TagNFCPublic(TagNFCBase):
        id: int