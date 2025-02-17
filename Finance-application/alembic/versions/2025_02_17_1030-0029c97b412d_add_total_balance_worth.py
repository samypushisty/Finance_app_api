"""add total balance worth

Revision ID: 0029c97b412d
Revises: b528346bb568
Create Date: 2025-02-17 10:30:39.373438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0029c97b412d'
down_revision: Union[str, None] = 'b528346bb568'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movie_on_account', sa.Column('total_balance_worth', sa.Numeric(precision=100, scale=2), nullable=False))


def downgrade() -> None:
    op.drop_column('movie_on_account', 'total_balance_worth')
