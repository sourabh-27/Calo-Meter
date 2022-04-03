"""Add column target_calories in user

Revision ID: 4736e0d298f1
Revises: 774281f0e195
Create Date: 2022-04-04 02:34:02.107826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4736e0d298f1'
down_revision = '774281f0e195'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('target_calories', sa.Integer(), server_default='2000', nullable=False))


def downgrade():
    op.drop_column('user', 'target_calories')
