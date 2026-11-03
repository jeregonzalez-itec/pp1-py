from datetime import datetime, timezone
from typing import  Optional
from sqlmodel import Field, Relationship, SQLModel

from .tagnfc import TagNFC
from .mascota import Mascota


class EscaneoTagBase(SQLModel):
    tag_id: int = Field(foreign_key="tagnfc.id")
    mascota_id: Optional[int] = Field(default=None, foreign_key="mascota.id")
    fecha_hora: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    latitud: Optional[float] = Field(default=None, description="Latitud GPS capturada por el navegador")
    longitud: Optional[float] = Field(default=None, description="Longitud GPS capturada por el navegador")
    direccion_aproximada: Optional[str] = Field(default=None)
    mensaje_rescatista: Optional[str] = Field(default=None, description="Mensaje opcional de quien encontró la mascota")
    telefono_rescatista: Optional[str] = Field(default=None, description="Teléfono de contacto opcional de quien la encontró")
   


class EscaneoTag(EscaneoTagBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    tag: Optional["TagNFC"] = Relationship(back_populates="escaneos")
    mascota: Optional["Mascota"] = Relationship(back_populates="escaneos")


class EscaneoTagPublic(EscaneoTagBase):
    id: int


class ReporteAvistamientoCreate(SQLModel):
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    mensaje: Optional[str] = Field(default=None, description="Mensaje para el dueño (ej: La tengo en la plaza)")
    telefono_contacto: Optional[str] = Field(default=None, description="Teléfono opcional para que el dueño te contacte")

