"""empty message

Revision ID: 27cbfbdcdcbd
Revises: 94f47c4bdbae
Create Date: 2021-11-28 23:20:04.906763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27cbfbdcdcbd'
down_revision = '94f47c4bdbae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
