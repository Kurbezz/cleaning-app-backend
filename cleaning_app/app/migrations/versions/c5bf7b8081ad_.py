"""empty message

Revision ID: c5bf7b8081ad
Revises: c020bbb9aed9
Create Date: 2021-10-03 01:24:26.957866

"""
from alembic import op
import sqlalchemy as sa
import ormar.fields.sqlalchemy_uuid


# revision identifiers, used by Alembic.
revision = "c5bf7b8081ad"
down_revision = "c020bbb9aed9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("description", sa.String(length=128), nullable=False),
        sa.Column("apartment", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["apartment"], ["apartments.id"], name="fk_tasks_apartments_id_apartment"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "completed_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task", sa.Integer(), nullable=True),
        sa.Column("complete_on", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["task"], ["tasks.id"], name="fk_completed_tasks_tasks_id_task"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_sheldules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task", sa.Integer(), nullable=True),
        sa.Column("sheldule", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task"], ["tasks.id"], name="fk_task_sheldules_tasks_id_task"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tasks_rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room", sa.Integer(), nullable=True),
        sa.Column("task", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["room"],
            ["rooms.id"],
            name="fk_tasks_rooms_rooms_room_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task"],
            ["tasks.id"],
            name="fk_tasks_rooms_tasks_task_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "shelduled_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task", sa.Integer(), nullable=True),
        sa.Column("task_sheldule", sa.Integer(), nullable=True),
        sa.Column("shelduled_to", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["task"], ["tasks.id"], name="fk_shelduled_tasks_tasks_id_task"
        ),
        sa.ForeignKeyConstraint(
            ["task_sheldule"],
            ["task_sheldules.id"],
            name="fk_shelduled_tasks_task_sheldules_id_task_sheldule",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shelduled_tasks")
    op.drop_table("tasks_rooms")
    op.drop_table("task_sheldules")
    op.drop_table("completed_tasks")
    op.drop_table("tasks")
    # ### end Alembic commands ###
