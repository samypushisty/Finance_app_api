"""add decimal

Revision ID: 822ce137caa5
Revises: 2ff84a6d3d89
Create Date: 2025-02-11 21:11:09.648238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '822ce137caa5'
down_revision: Union[str, None] = '2ff84a6d3d89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('balance', 'total_balance',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Numeric(precision=100, scale=2),
               existing_nullable=False)
    op.alter_column('movie_on_account', 'worth',
                    existing_type=sa.Numeric(),
                    type_=sa.Numeric(precision=100, scale=2),
                    existing_nullable=False)
    op.alter_column('cash_account', 'balance',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Numeric(precision=100, scale=2),
               existing_nullable=False)


def downgrade() -> None:
    op.alter_column('cash_account', 'balance',
               existing_type=sa.Numeric(precision=100, scale=2),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    op.alter_column('movie_on_account', 'worth',
                    existing_type=sa.Numeric(precision=100, scale=2),
                    type_=sa.Numeric(),
                    existing_nullable=False)
    op.alter_column('balance', 'total_balance',
               existing_type=sa.Numeric(precision=100, scale=2),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
