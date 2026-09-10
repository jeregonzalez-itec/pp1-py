from typing import Annotated

from pydantic import Field


Titulo = Annotated[str, Field(max_length=30)]
PrecioPublico = Annotated[int, Field(gt=500, lt=999999)]
Stock = Annotated[int, Field(gt=0)]
Material = Annotated[str, Field(max_length=30)]
Descripcion = Annotated[str, Field(max_length=30)]
Disponible = Annotated[bool, Field(description="Sigue disponible?")]