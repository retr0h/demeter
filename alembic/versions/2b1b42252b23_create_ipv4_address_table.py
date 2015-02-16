"""create ipv4_address table

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
        'ipv4_address',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('namespace', sa.String(25), nullable=False),
        sa.Column('cidr', postgresql.CIDR, nullable=False),
        sa.Column('address', postgresql.INET, nullable=False),
        sa.Column('allocated', sa.Boolean, server_default='0'),
        # getconf HOST_NAME_MAX
        sa.Column('hostname', sa.String(64)),

        sa.UniqueConstraint('namespace', 'hostname', name='uix_1')
    )


def downgrade():
    op.drop_table('ipv4_address')
