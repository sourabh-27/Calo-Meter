"""Add timestamps

Revision ID: 51dce7514162
Revises: cbb09e666beb
Create Date: 2022-04-04 02:57:28.597531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51dce7514162'
down_revision = 'cbb09e666beb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))
    op.add_column('item', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))
    op.add_column('item', sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))


def downgrade():
    op.drop_column('item', 'updated_at')
    op.drop_column('item', 'created_at')
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'created_at')
