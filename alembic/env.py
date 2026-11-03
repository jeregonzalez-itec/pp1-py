from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# ---------------------------------------------------------------------------
# Asegurar que src/ esté en sys.path para poder importar los modelos
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Importar todos los modelos con tabla para que SQLModel.metadata los registre.
# Si se agrega un modelo nuevo, importarlo aquí también.
from models.usuario import Usuario          # noqa: F401
from models.mascota import Mascota          # noqa: F401
from models.tagnfc import TagNFC            # noqa: F401
from models.veterinaria import Veterinaria  # noqa: F401
from models.escaneo import EscaneoTag       # noqa: F401

# ---------------------------------------------------------------------------
# Configuración de Alembic
# ---------------------------------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de SQLModel — usada por autogenerate
target_metadata = SQLModel.metadata


# ---------------------------------------------------------------------------
# Helpers de migración
# ---------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Modo offline: genera el SQL sin conexión a la base de datos.
    Útil para revisar el script antes de aplicarlo.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # render_as_batch: necesario para SQLite, que no soporta ALTER COLUMN nativo.
        # Alembic recrea la tabla completa en background para aplicar los cambios.
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Modo online: se conecta a la base de datos y aplica las migraciones directamente.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # render_as_batch: requerido para SQLite.
            # Para PostgreSQL / MySQL se puede dejar en False sin problema.
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
