"""agregar_escaneo_y_flujo_reclamo

Revision ID: 357850932261
Revises: 240114c9b781
Create Date: 2026-10-30 17:01:47.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '357850932261'
down_revision: Union[str, Sequence[str], None] = '240114c9b781'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
