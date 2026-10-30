"""Migracion inicial

Revision ID: a1c4f7d92b30
Revises:
Create Date: 2026-10-25 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1c4f7d92b30"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

S = sqlmodel.sql.sqltypes.AutoString


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "usuario",
        sa.Column("nombre", S(length=90), nullable=False),
        sa.Column("email", S(length=120), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contraseña", S(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "veterinaria",
        sa.Column("nombre", S(length=90), nullable=False),
        sa.Column("telefono", S(length=30), nullable=False),
        sa.Column("direccion", S(length=150), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tagnfc",
        sa.Column("codigo_qr", S(length=60), nullable=False),
        sa.Column("uid_nfc", S(length=60), nullable=False),
        sa.Column("precio", sa.Integer(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column("veterinaria_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["veterinaria_id"], ["veterinaria.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_qr"),
        sa.UniqueConstraint("uid_nfc"),
    )
    op.create_table(
        "mascota",
        sa.Column("nombre", S(length=60), nullable=False),
        sa.Column("especie", S(length=40), nullable=False),
        sa.Column("raza", S(length=60), nullable=False),
        sa.Column("estado", sa.Boolean(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=True),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["tag_id"], ["tagnfc.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tag_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("mascota")
    op.drop_table("tagnfc")
    op.drop_table("veterinaria")
    op.drop_table("usuario")
