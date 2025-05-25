"""update field base_worth

Revision ID: cd2ad9bba2d0
Revises: 261366795c8a
Create Date: 2025-02-22 19:28:15.718344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd2ad9bba2d0'
down_revision: Union[str, None] = '261366795c8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movie_on_account', sa.Column('base_worth', sa.Numeric(precision=100, scale=2), nullable=False))
    op.drop_column('movie_on_account', 'main_account_worth')
    op.drop_column('movie_on_account', 'cash_account_worth')


def downgrade() -> None:
    op.add_column('movie_on_account', sa.Column('cash_account_worth', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False))
    op.add_column('movie_on_account', sa.Column('main_account_worth', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False))
    op.drop_column('movie_on_account', 'base_worth')
