
from .mate import Mate ,MatePublic
from .proveedor import ProveedorPublic, Proveedor

#Articulo Anidado
class MateNested(MatePublic):
    proveedor: Proveedor | None = None


class ProveedorNested(ProveedorPublic):
    articulos: list[Mate] = []