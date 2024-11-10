"""Fixing Diver Gears

Revision ID: f54eada9f746
Revises: 552e97dba1b5
Create Date: 2024-11-10 17:01:27.865944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f54eada9f746'
down_revision: Union[str, None] = '552e97dba1b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('diver_gears', sa.Column('master_brand_id', sa.Integer(), nullable=False))
    op.drop_constraint('diver_gears_ibfk_3', 'diver_gears', type_='foreignkey')
    op.create_foreign_key(None, 'diver_gears', 'master_brands', ['master_brand_id'], ['id'])
    op.drop_column('diver_gears', 'master_gears_brand_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('diver_gears', sa.Column('master_gears_brand_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'diver_gears', type_='foreignkey')
    op.create_foreign_key('diver_gears_ibfk_3', 'diver_gears', 'master_gears_brands', ['master_gears_brand_id'], ['id'])
    op.drop_column('diver_gears', 'master_brand_id')
    # ### end Alembic commands ###
