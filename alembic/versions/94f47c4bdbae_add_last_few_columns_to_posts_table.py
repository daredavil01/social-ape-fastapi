"""add last few columns to posts table

Revision ID: 94f47c4bdbae
Revises: b2e25176616e
Create Date: 2021-11-28 23:11:40.562116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94f47c4bdbae'
down_revision = 'b2e25176616e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean,
                  nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
