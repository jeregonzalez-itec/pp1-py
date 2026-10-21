
from .tagnfc import Mate ,MatePublic
from .veterinaria import ProveedorPublic, Proveedor

#Articulo Anidado
class MateNested(MatePublic):
    proveedor: Proveedor | None = None


class ProveedorNested(ProveedorPublic):
    articulos: list[Mate] = []