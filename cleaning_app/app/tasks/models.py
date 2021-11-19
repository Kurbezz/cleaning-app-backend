from datetime import datetime
from typing import Optional

from sqlalchemy import text
import ormar

from core.db import BaseMeta
from app.apartments.models import Apartment, Room
from app.users.models import User


class Task(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tasks"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    name: str = ormar.String(max_length=32)  # type: ignore
    description: str = ormar.String(max_length=128)  # type: ignore
    apartment: Apartment = ormar.ForeignKey(Apartment, ondelete="CASCADE")
    rooms = ormar.ManyToMany(Room)
    points: int = ormar.SmallInteger(default=0, minimum=0, server_default=text("0"), nullable=False)  # type: ignore
    is_archived: bool = ormar.Boolean(
        default=False, server_default=text("false"), nullable=False
    )


class TaskSchedule(ormar.Model):
    class Meta(BaseMeta):
        tablename = "task_sheldules"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task, ondelete="CASCADE")
    schedule = ormar.JSON()
    executors = ormar.ManyToMany(User)


class ScheduledTask(ormar.Model):
    class Meta(BaseMeta):
        tablename = "shelduled_tasks"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task, ondelete="CASCADE")
    task_schedule: Optional[TaskSchedule] = ormar.ForeignKey(
        TaskSchedule, ondelete="CASCADE"
    )
    scheduled_to: datetime = ormar.DateTime(timezone=True)  # type: ignore


class CompletedTask(ormar.Model):
    class Meta(BaseMeta):
        tablename = "completed_tasks"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task, ondelete="CASCADE")
    scheduled_task: Optional[ScheduledTask] = ormar.ForeignKey(
        ScheduledTask, nullable=True, ondelete="SET NULL"
    )
    complete_on: datetime = ormar.DateTime(timezone=True)  # type: ignore
    executors = ormar.ManyToMany(User)
