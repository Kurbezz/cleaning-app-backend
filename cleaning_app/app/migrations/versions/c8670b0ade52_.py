"""empty message

Revision ID: c8670b0ade52
Revises: 1e1c9d7bcc4b
Create Date: 2021-10-17 11:37:42.912755

"""
from alembic import op
import sqlalchemy as sa
import ormar.fields.sqlalchemy_uuid


# revision identifiers, used by Alembic.
revision = 'c8670b0ade52'
down_revision = '1e1c9d7bcc4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('points', sa.SmallInteger(), server_default=sa.text("0"), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'points')
    # ### end Alembic commands ###
