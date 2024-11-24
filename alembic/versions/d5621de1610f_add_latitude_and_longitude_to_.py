"""Add latitude and longitude to collections and cooperative

Revision ID: d5621de1610f
Revises: 5b1ed032c37d
Create Date: 2024-11-24 14:53:45.623324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5621de1610f'
down_revision: Union[str, None] = '5b1ed032c37d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collections', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('collections', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('cooperative', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('cooperative', sa.Column('longitude', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cooperative', 'longitude')
    op.drop_column('cooperative', 'latitude')
    op.drop_column('collections', 'longitude')
    op.drop_column('collections', 'latitude')
    # ### end Alembic commands ###