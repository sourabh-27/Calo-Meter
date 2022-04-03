"""Add column calories in items

Revision ID: cbb09e666beb
Revises: 4736e0d298f1
Create Date: 2022-04-04 02:41:20.881304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbb09e666beb'
down_revision = '4736e0d298f1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('item', sa.Column('calories', sa.Integer(), server_default=sa.text('0'), nullable=False))


def downgrade():
    op.drop_column('item', 'calories')
