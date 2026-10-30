"""Schemas Nested: devuelven el registro junto con sus relaciones."""
from .mascota import MascotaPublic
from .tagnfc import TagNFCPublic
from .usuario import UsuarioPublic
from .veterinaria import VeterinariaPublic


class VeterinariaNested(VeterinariaPublic):
    tags: list[TagNFCPublic] = []


class TagNFCNested(TagNFCPublic):
    veterinaria: VeterinariaPublic | None = None
    mascota: MascotaPublic | None = None


class MascotaNested(MascotaPublic):
    tag: TagNFCPublic | None = None
    usuario: UsuarioPublic | None = None


class UsuarioNested(UsuarioPublic):
    mascotas: list[MascotaPublic] = []
