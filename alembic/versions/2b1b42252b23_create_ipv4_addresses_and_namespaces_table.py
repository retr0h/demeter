"""create ipv4_addresses and namespaces table

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
        'namespaces',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(36), nullable=False),
        sa.Column('cidr', postgresql.CIDR, nullable=False),

        sa.UniqueConstraint('name', name='name_uix'),
    )

    op.create_table(
        'ipv4_addresses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', postgresql.INET, nullable=False),
        sa.Column('address_int', sa.Numeric(10), nullable=False),
        # getconf HOST_NAME_MAX
        sa.Column('hostname', sa.String(64)),
        sa.Column('namespace_id',
                  sa.Integer,
                  sa.ForeignKey('namespaces.id'),
                  primary_key=True),
    )


def downgrade():
    op.drop_table('ipv4_addresses')
    op.drop_table('namespaces')
