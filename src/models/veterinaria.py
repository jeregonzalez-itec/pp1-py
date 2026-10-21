from sqlmodel import Field, Relationship, SQLModel


# Consultar articulos.py para explicación más detallada
class VeterinariaBase(SQLModel):
    nombre: str = Field(max_length=90)
    telefono: str


class Veterinaria(VeterinariaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Para evitar import circular, Articulo va en str
    mates: list["TagNFC"] | None = Relationship(back_populates="veterinaria")


class VeterinariaPublic(VeterinariaBase):
    id: int