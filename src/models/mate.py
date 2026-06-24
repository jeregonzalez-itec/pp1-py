from typing import Annotated
from pydantic import BaseModel, Field

class MateBase(BaseModel):
    nombre: Annotated[
        str,
        Field(description="Nombre del mate")
    ]

    material: Annotated[
        str,
        Field(description="Material del mate")
    ]

    precio: Annotated[
        float,
        Field(gt=0, description="Precio del mate")
    ]

    stock: Annotated[
        int,
        Field(ge=0, description="Cantidad disponible")
    ]


class Mate(MateBase):
    id: Annotated[
        int,
        Field(description="ID del mate")
    ]
