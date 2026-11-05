from typing import Optional
from sqlmodel import SQLModel

from .mascota import MascotaPublic
from .tagnfc import TagNFCPublic
from .usuario import UsuarioPublic
from .veterinaria import VeterinariaPublic


# Modelos con relaciones anidadas para respuestas detalladas de endpoints GET /{id}

class UsuarioNested(UsuarioPublic):
    mascotas: list[MascotaPublic] = []


class MascotaNested(MascotaPublic):
    tag: Optional[TagNFCPublic] = None
    usuario: Optional[UsuarioPublic] = None


class TagNFCNested(TagNFCPublic):
    veterinaria: Optional[VeterinariaPublic] = None
    mascota: Optional[MascotaPublic] = None


class VeterinariaNested(VeterinariaPublic):
    tags: list[TagNFCPublic] = []


# Esquemas específicos para el flujo público de escaneo y reclamo

class ContactoDuenoPublic(SQLModel):
    nombre: str
    telefono: Optional[str] = None
    telefono_secundario: Optional[str] = None
    whatsapp_url: Optional[str] = None


class PerfilMascotaScan(SQLModel):
    id: int
    nombre: str
    especie: str
    raza: str
    color: Optional[str] = None
    foto_url: Optional[str] = None
    estado_extravio: str
    notas_medicas: Optional[str] = None
    mensaje_personalizado: Optional[str] = None
    recompensa: Optional[str] = None
    contacto: Optional[ContactoDuenoPublic] = None


class TagScanResult(SQLModel):
    reclamado: bool
    token_publico: str
    codigoQR: str
    estado_tag: str
    mensaje: str
    mascota: Optional[PerfilMascotaScan] = None
    veterinaria: Optional[VeterinariaPublic] = None


class ReclamarTagRequest(SQLModel):
    token_o_codigo: str
    nombre_mascota: str
    especie: str = "Perro"
    raza: str = "Mestizo"
    color: Optional[str] = None
    foto_url: Optional[str] = None
    notas_medicas: Optional[str] = None
    mensaje_personalizado: Optional[str] = None
    mostrar_telefono: bool = True
