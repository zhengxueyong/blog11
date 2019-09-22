"""empty message

Revision ID: 78080733bd1e
Revises: f4a1b28d4458
Create Date: 2019-03-28 09:51:05.451044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78080733bd1e'
down_revision = 'f4a1b28d4458'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.Column('icon', sa.String(length=256), nullable=True),
    sa.Column('isactive', sa.Boolean(), nullable=True),
    sa.Column('isdelte', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###