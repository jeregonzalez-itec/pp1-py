from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel


from src.models.veterinaria import Veterinaria
from src.models.tagnfc import TagNFC           
from src.models.usuario import Usuario       
from src.models.mascota import Mascota         
from src.models.escaneo import EscaneoTag     

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
