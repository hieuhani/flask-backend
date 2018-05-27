"""create contacts table

Revision ID: 78413bdbf90c
Revises: 51782f2f7a5a
Create Date: 2018-05-26 17:32:08.462914

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '78413bdbf90c'
down_revision = '51782f2f7a5a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'contacts',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('type', sa.SmallInteger, nullable=False),
        sa.Column('value', sa.String, nullable=False),
        sa.Column('verified', sa.Boolean, nullable=False, default=False),
    )


def downgrade():
    op.drop_table('contacts')
