"""Alter user_id to String type for UUID

Revision ID: 950f99ce7d8c
Revises: ea277f74be62
Create Date: 2024-11-08 14:53:57.387349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '950f99ce7d8c'
down_revision: Union[str, None] = 'ea277f74be62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
