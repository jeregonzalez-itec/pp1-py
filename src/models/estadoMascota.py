from enum import Enum


class EstadoMascotaEnum(str, Enum):
    EN_CASA = "en_casa"
    PERDIDO = "perdido"
    ENCONTRADO = "encontrado"
    EN_VETERINARIA = "en_veterinaria"
    EN_ADOPCION = "en_adopcion"


class EstadoTagEnum(str, Enum):
    DISPONIBLE = "disponible"  # En stock, virgen para ser reclamado
    RECLAMADO = "reclamado"    # Vinculado a una mascota activa
    EXTRAVIADO = "extraviado"  # Mascota perdida o chapita extraviada
    INACTIVO = "inactivo"      # De baja por rotura o reemplazo


class RolUsuarioEnum(str, Enum):
    DUENO = "dueno"
    VETERINARIA = "veterinaria"
    ADMIN = "admin"
