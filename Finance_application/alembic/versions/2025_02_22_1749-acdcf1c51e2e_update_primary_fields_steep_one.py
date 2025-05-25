"""update primary fields steep one

Revision ID: acdcf1c51e2e
Revises: 8618fc4f7d38
Create Date: 2025-02-22 17:49:25.656216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'acdcf1c51e2e'
down_revision: Union[str, None] = '8618fc4f7d38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('movie_on_account')
    op.drop_table('earnings')
    op.drop_table('cash_account')
    op.drop_table('category')




def downgrade() -> None:
    op.create_table('category',
    sa.Column('category_id', sa.INTEGER(), server_default=sa.text("nextval('category_category_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('month_limit', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('balance', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name='fk_category_chat_id_user', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('category_id', name='pk_category'),
    postgresql_ignore_search_path=False
    )
    op.create_table('cash_account',
    sa.Column('cash_id', sa.INTEGER(), server_default=sa.text("nextval('cash_account_cash_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('balance', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('type', postgresql.ENUM('cash', 'card', name='cashaccounttype'), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name='fk_cash_account_chat_id_user', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('cash_id', name='pk_cash_account'),
    postgresql_ignore_search_path=False
    )
    op.create_table('movie_on_account',
    sa.Column('movie_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('type', postgresql.ENUM('earning', 'outlay', name='movietype'), autoincrement=False, nullable=False),
    sa.Column('worth', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False),
    sa.Column('cash_account', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('categories_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('earnings_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('time', postgresql.TIMESTAMP(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.Column('cash_account_worth', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False),
    sa.Column('main_account_worth', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cash_account'], ['cash_account.cash_id'], name='fk_movie_on_account_cash_account_cash_account', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['categories_id'], ['category.category_id'], name='fk_movie_on_account_categories_id_category', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name='fk_movie_on_account_chat_id_user', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['earnings_id'], ['earnings.earning_id'], name='fk_movie_on_account_earnings_id_earnings', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('movie_id', name='pk_movie_on_account')
    )
    op.create_table('earnings',
    sa.Column('chat_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('earning_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('balance', sa.NUMERIC(precision=100, scale=2), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], name='fk_earnings_chat_id_user', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('earning_id', name='pk_earnings')
    )

