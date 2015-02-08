"""create address and tag tables

Revision ID: 2b1b42252b23
Revises: None
Create Date: 2015-02-09 00:19:18.157283

"""

# revision identifiers, used by Alembic.
revision = '2b1b42252b23'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        'tag',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(25), nullable=False, unique=True),
    )
    op.create_table(
        'address',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', postgresql.CIDR, nullable=False),
        sa.Column('family', sa.String(4), nullable=False),
        sa.Column('tag_id',
                  sa.Integer,
                  sa.ForeignKey('tag.id'),
                  primary_key=True),
    )


def downgrade():
    op.drop_table('address')
    op.drop_table('tag')
