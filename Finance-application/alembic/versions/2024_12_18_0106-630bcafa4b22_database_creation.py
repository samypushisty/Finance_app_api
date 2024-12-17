"""database creation

Revision ID: 630bcafa4b22
Revises: 
Create Date: 2024-12-18 01:06:33.233470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = '630bcafa4b22'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('currencies', sa.String(), nullable=False),
    sa.Column('type_of_earnings', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('chat_id', name=op.f('pk_user'))
    )
    op.create_table('balance',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('total_balance', sa.Float(), nullable=False),
    sa.Column('balances_history', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_balance_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('chat_id', name=op.f('pk_balance'))
    )
    op.create_table('cash_account',
    sa.Column('cash_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('type', sa.Enum('cash', 'card', name='cashaccounttype'), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_cash_account_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('cash_id', name=op.f('pk_cash_account'))
    )
    op.create_table('category',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('month_limit', sa.Float(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_category_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('chat_id', name=op.f('pk_category'))
    )
    op.create_table('settings',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('theme', sa.Enum('black', 'white', 'auto', name='theme'), nullable=False),
    sa.Column('language', sa.Enum('english', 'russian', name='language'), nullable=False),
    sa.Column('notifications', sa.Boolean(), nullable=False),
    sa.Column('main_currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_settings_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('chat_id', name=op.f('pk_settings'))
    )
    op.create_table('movie_on_account',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=15), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('type', sa.Enum('earning', 'outlay', name='movietype'), nullable=False),
    sa.Column('worth', sa.Numeric(), nullable=False),
    sa.Column('cash_account', sa.Integer(), nullable=False),
    sa.Column('categories_name', sa.String(), nullable=True),
    sa.Column('earnings_type', sa.String(), nullable=True),
    sa.Column('time', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['cash_account'], ['cash_account.cash_id'], name=op.f('fk_movie_on_account_cash_account_cash_account'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name=op.f('fk_movie_on_account_chat_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('movie_id', name=op.f('pk_movie_on_account'))
    )


def downgrade() -> None:
    op.drop_table('movie_on_account')
    op.drop_table('settings')
    op.drop_table('category')
    op.drop_table('cash_account')
    op.drop_table('balance')
    op.drop_table('user')
