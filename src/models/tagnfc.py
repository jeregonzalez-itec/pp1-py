from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel

from .estadoMascota import EstadoTagEnum
from .veterinaria import Veterinaria
from .mascota import Mascota
from .escaneo import EscaneoTag


def generar_token_publico() -> str:
    """Genera un identificador público corto y único para la URL del QR/NFC (ej: enc-8f12a4b3)."""
    return f"enc-{uuid.uuid4().hex[:8]}"


class TagNFCBase(SQLModel):
    codigoQR: str = Field(unique=True, index=True, description="Código de serie impreso en el QR")
    uidNFC: str = Field(unique=True, index=True, description="UID físico del chip NFC")
    token_publico: str = Field(
        default_factory=generar_token_publico,
        unique=True,
        index=True,
        description="Token público para la URL de escaneo /scan/{token_publico}",
    )
    precio: int = Field(default=5000)
    activo: bool = Field(default=True)
    estado: str = Field(default=EstadoTagEnum.DISPONIBLE, description="disponible, reclamado, extraviado, inactivo")
    fecha_activacion: Optional[datetime] = Field(default=None)
    veterinaria_id: Optional[int] = Field(default=None, foreign_key="veterinaria.id")


class TagNFC(TagNFCBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    veterinaria: Optional["Veterinaria"] = Relationship(back_populates="tags")
    mascota: Optional["Mascota"] = Relationship(back_populates="tag")
    escaneos: list["EscaneoTag"] = Relationship(back_populates="tag")


class TagNFCPublic(TagNFCBase):
    id: int
