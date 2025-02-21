"""add currencies to table

Revision ID: 29b53a6f73e1
Revises: 4752a25c9238
Create Date: 2025-02-21 11:06:57.483684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29b53a6f73e1'
down_revision: Union[str, None] = '4752a25c9238'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('category', sa.Column('balance', sa.Numeric(precision=100, scale=2), nullable=False))
    op.add_column('category', sa.Column('currency', sa.String(length=3), nullable=False))
    op.add_column('earnings', sa.Column('balance', sa.Numeric(precision=100, scale=2), nullable=False))
    op.add_column('earnings', sa.Column('currency', sa.String(length=3), nullable=False))


def downgrade() -> None:
    op.drop_column('earnings', 'currency')
    op.drop_column('earnings', 'balance')
    op.drop_column('category', 'currency')
    op.drop_column('category', 'balance')
