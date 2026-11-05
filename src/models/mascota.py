from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from .estadoMascota import EstadoMascotaEnum

if TYPE_CHECKING:
    from .escaneo import EscaneoTag
    from .tagnfc import TagNFC
    from .usuario import Usuario


class MascotaBase(SQLModel):
    nombre: str
    especie: str = Field(default="Perro", description="Perro, Gato, etc.")
    raza: str = Field(default="Mestizo")
    color: Optional[str] = Field(default=None)
    foto_url: Optional[str] = Field(default=None, description="URL de la foto de la mascota para el perfil público")
    estado_extravio: str = Field(
        default=EstadoMascotaEnum.EN_CASA,
        description="en_casa, perdido, encontrado, en_veterinaria, en_adopcion",
    )
    notas_medicas: Optional[str] = Field(
        default=None,
        description="Indicaciones médicas críticas (ej: Requiere medicación diaria, es ciego/sordo, diabético)",
    )
    mensaje_personalizado: Optional[str] = Field(
        default=None,
        description="Mensaje del dueño que verá quien escanee la chapita",
    )
    mostrar_telefono: bool = Field(default=True, description="Mostrar botón de WhatsApp/llamada directo")
    mostrar_direccion: bool = Field(default=False, description="Mostrar dirección aproximada del hogar")
    recompensa: Optional[str] = Field(default=None, description="Monto o detalle de recompensa si aplica")
    estado: bool = Field(default=True, description="Baja lógica del registro (True=activo)")
    tag_id: Optional[int] = Field(default=None, foreign_key="tagnfc.id", unique=True)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")


class Mascota(MascotaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tag: Optional["TagNFC"] = Relationship(back_populates="mascota")
    usuario: Optional["Usuario"] = Relationship(back_populates="mascotas")
    escaneos: list["EscaneoTag"] = Relationship(back_populates="mascota")


class MascotaPublic(MascotaBase):
    id: int
