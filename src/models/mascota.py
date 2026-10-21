from sqlmodel import Field, SQLModel, Relationship
from .tagnfc import TagNFC
class MascotaBase(SQLModel):
    nombre: str
    especie: str
    raza: str
    estado: bool
    tagnfc_id: int | None = Field(default=None, foreign_key="tagnfc.id" )


class Mascota(MascotaBase,table = True):
       id: int | None = Field(default=None, primary_key=True)
       tagnfc: TagNFC | None = Relationship(back_populates="tagnfc")

class MascotaPublic(MascotaBase):
        id: int