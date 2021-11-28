"""add foreign key to posts table

Revision ID: b2e25176616e
Revises: b5603e1e2e6c
Create Date: 2021-11-28 23:06:41.642289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2e25176616e'
down_revision = 'b5603e1e2e6c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_owner_id', source_table='posts',
                          referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('fk_posts_owner_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
