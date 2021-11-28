"""create post table

Revision ID: 813a6cfa44a6
Revises: 
Create Date: 2021-11-28 22:39:15.406571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '813a6cfa44a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
