"""update primary fields steep last

Revision ID: 261366795c8a
Revises: acdcf1c51e2e
Create Date: 2025-02-22 17:57:43.623578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '261366795c8a'
down_revision: Union[str, None] = 'acdcf1c51e2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cash_account',
    sa.Column('table_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('balance', sa.Numeric(precision=100, scale=2), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('type', sa.Enum('cash', 'card', name='cashaccounttype'), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_cash_account_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('table_id', name=op.f('pk_cash_account'))
    )
    op.create_table('category',
    sa.Column('table_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('month_limit', sa.Float(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('balance', sa.Numeric(precision=100, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_category_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('table_id', name=op.f('pk_category'))
    )
    op.create_table('earnings',
    sa.Column('table_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('balance', sa.Numeric(precision=100, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_earnings_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('table_id', name=op.f('pk_earnings'))
    )
    op.create_table('movie_on_account',
    sa.Column('table_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=15), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('type', sa.Enum('earning', 'outlay', name='movietype'), nullable=False),
    sa.Column('worth', sa.Numeric(precision=100, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('cash_account_worth', sa.Numeric(precision=100, scale=2), nullable=False),
    sa.Column('main_account_worth', sa.Numeric(precision=100, scale=2), nullable=False),
    sa.Column('cash_account', sa.Integer(), nullable=False),
    sa.Column('categories_id', sa.Integer(), nullable=True),
    sa.Column('earnings_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['cash_account'], ['cash_account.table_id'], name=op.f('fk_movie_on_account_cash_account_cash_account'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['categories_id'], ['category.table_id'], name=op.f('fk_movie_on_account_categories_id_category'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_movie_on_account_chat_id_user'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['earnings_id'], ['earnings.table_id'], name=op.f('fk_movie_on_account_earnings_id_earnings'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('table_id', name=op.f('pk_movie_on_account'))
    )


def downgrade() -> None:
    op.drop_table('movie_on_account')
    op.drop_table('earnings')
    op.drop_table('category')
    op.drop_table('cash_account')
