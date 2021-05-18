"""empty message

Revision ID: 3408793f3885
Revises: e2c3ae6b4f62
Create Date: 2021-05-17 22:52:58.189289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3408793f3885'
down_revision = 'e2c3ae6b4f62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('MemeTemplate',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('image_path', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_index(op.f('ix_MemeTemplate_title'), 'MemeTemplate', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_MemeTemplate_title'), table_name='MemeTemplate')
    op.drop_table('MemeTemplate')
    # ### end Alembic commands ###