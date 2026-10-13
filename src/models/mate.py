from sqlmodel import Field, SQLModel, Relationship
from .proveedor import Proveedor
class MateBase(SQLModel):
    nombre: str = Field(max_length=90)
    stock: int | None
    precio: int
    activo: bool
    proveedor_id: int | None = Field(default=None, foreign_key="proveedor.id" )


class Mate(MateBase,table = True):
       id: int | None = Field(default=None, primary_key=True)
       proveedor: Proveedor | None = Relationship(back_populates="mates")

class MatePublic(MateBase):
        id: int