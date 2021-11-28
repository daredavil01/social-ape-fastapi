"""add content column to posts table

Revision ID: 947384f54f6b
Revises: 6f22d6c7b317
Create Date: 2021-11-28 22:52:47.169172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '947384f54f6b'
down_revision = '813a6cfa44a6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
