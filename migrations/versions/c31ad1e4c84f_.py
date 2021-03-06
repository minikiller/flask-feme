"""empty message

Revision ID: c31ad1e4c84f
Revises: 65c7065f3f79
Create Date: 2021-03-04 14:25:57.247959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c31ad1e4c84f'
down_revision = '65c7065f3f79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('application', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('setting')
    # ### end Alembic commands ###
