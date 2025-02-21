"""add FK to movie table 

Revision ID: 4752a25c9238
Revises: acae6d8b5448
Create Date: 2025-02-21 09:11:59.098024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4752a25c9238'
down_revision: Union[str, None] = 'acae6d8b5448'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(op.f('fk_movie_on_account_categories_id_category'), 'movie_on_account', 'category', ['categories_id'], ['category_id'], ondelete='CASCADE')
    op.create_foreign_key(op.f('fk_movie_on_account_earnings_id_earnings'), 'movie_on_account', 'earnings', ['earnings_id'], ['earning_id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(op.f('fk_movie_on_account_earnings_id_earnings'), 'movie_on_account', type_='foreignkey')
    op.drop_constraint(op.f('fk_movie_on_account_categories_id_category'), 'movie_on_account', type_='foreignkey')
