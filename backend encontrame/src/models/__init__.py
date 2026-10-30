# Importar TODOS los modelos acá asegura que SQLAlchemy resuelva las
# relaciones (referencias en str) y que Alembic los detecte.
from .mascota import Mascota
from .tagnfc import TagNFC
from .usuario import Usuario
from .veterinaria import Veterinaria

__all__ = ["Mascota", "TagNFC", "Usuario", "Veterinaria"]
