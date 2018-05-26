"""create users table

Revision ID: 51782f2f7a5a
Revises:
Create Date: 2018-05-26 17:31:53.333499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '51782f2f7a5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID, primary_key=True),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('users')
