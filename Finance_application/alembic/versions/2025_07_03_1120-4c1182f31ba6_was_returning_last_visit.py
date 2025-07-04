"""was returning last visit

Revision ID: 4c1182f31ba6
Revises: 4d4a478476ae
Create Date: 2025-07-03 11:20:08.183514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4c1182f31ba6'
down_revision: Union[str, None] = '4d4a478476ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('balance', 'balances_history',
               existing_type=postgresql.ARRAY(sa.NUMERIC(precision=19, scale=4)),
               type_=sa.ARRAY(sa.Numeric(precision=19, scale=2)),
               existing_nullable=False,
               existing_server_default=sa.text("'{}'::numeric[]"))
    op.drop_column('balance', 'last_visit')
    op.add_column('user', sa.Column('last_visit', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_visit')
    op.add_column('balance', sa.Column('last_visit', postgresql.TIMESTAMP(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False))
    op.alter_column('balance', 'balances_history',
               existing_type=sa.ARRAY(sa.Numeric(precision=19, scale=2)),
               type_=postgresql.ARRAY(sa.NUMERIC(precision=19, scale=4)),
               existing_nullable=False,
               existing_server_default=sa.text("'{}'::numeric[]"))
    # ### end Alembic commands ###
