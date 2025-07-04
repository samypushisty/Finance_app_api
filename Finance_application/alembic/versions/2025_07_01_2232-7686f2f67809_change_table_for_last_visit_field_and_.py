"""change table for last visit field and del balances history for change type

Revision ID: 7686f2f67809
Revises: ae7c0a77a946
Create Date: 2025-07-01 22:32:33.940269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7686f2f67809'
down_revision: Union[str, None] = 'ae7c0a77a946'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('balance', sa.Column('last_visit', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False))
    op.drop_column('balance', 'balances_history')
    op.drop_column('user', 'last_visit')

def downgrade() -> None:
    op.add_column('user', sa.Column('last_visit', postgresql.TIMESTAMP(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False))
    op.add_column('balance', sa.Column('balances_history', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('balance', 'last_visit')
