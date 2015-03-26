"""create family column

Revision ID: 271caf775a05
Revises: 2b1b42252b23
Create Date: 2015-03-27 00:06:48.970495

"""

# revision identifiers, used by Alembic.
revision = '271caf775a05'
down_revision = '2b1b42252b23'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('namespaces', sa.Column('family',
                                          sa.String(5),
                                          nullable=False))


def downgrade():
    op.drop_column('namespaces', 'family')
