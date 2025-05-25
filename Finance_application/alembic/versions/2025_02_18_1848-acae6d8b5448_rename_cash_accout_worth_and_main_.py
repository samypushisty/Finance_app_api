"""rename cash_accout_worth and main_account_worth

Revision ID: acae6d8b5448
Revises: 0029c97b412d
Create Date: 2025-02-18 18:48:03.208501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acae6d8b5448'
down_revision: Union[str, None] = '0029c97b412d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movie_on_account', sa.Column('cash_account_worth', sa.Numeric(precision=100, scale=2), nullable=False))
    op.add_column('movie_on_account', sa.Column('main_account_worth', sa.Numeric(precision=100, scale=2), nullable=False))
    op.drop_column('movie_on_account', 'total_balance_worth')
    op.drop_column('movie_on_account', 'base_worth')


def downgrade() -> None:
    op.add_column('movie_on_account', sa.Column('base_worth', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False))
    op.add_column('movie_on_account', sa.Column('total_balance_worth', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False))
    op.drop_column('movie_on_account', 'main_account_worth')
    op.drop_column('movie_on_account', 'cash_account_worth')
