"""empty message

Revision ID: fc06769379e7
Revises: c8670b0ade52
Create Date: 2021-11-03 19:04:29.307998

"""
from alembic import op
import sqlalchemy as sa
import ormar.fields.sqlalchemy_uuid


# revision identifiers, used by Alembic.
revision = 'fc06769379e7'
down_revision = 'c8670b0ade52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_sheldules', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_sheldules', 'is_deleted')
    # ### end Alembic commands ###
