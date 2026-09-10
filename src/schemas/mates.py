from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from .tipos import Descripcion, Disponible, Material, PrecioPublico, Stock, Titulo

class MateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(gt=0, description="ID del mate")]
    nombre: Titulo
    precio: PrecioPublico = 1500
    stock: Stock = 0
    material: Material
    descripcion: Descripcion 
    disponible: Disponible = True


class MateUpdateSchema(BaseModel):
    nombre: Titulo
    precio: PrecioPublico = 2000
    stock: Stock = 0
    material: Material 
    descripcion: Descripcion 
    disponible: Disponible = True