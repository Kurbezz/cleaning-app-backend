from datetime import datetime
from typing import Optional

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
    apartment: Apartment = ormar.ForeignKey(Apartment)
    rooms = ormar.ManyToMany(Room)
    points: int = ormar.SmallInteger(default=0, minimum=0)  # type: ignore


class TaskSchedule(ormar.Model):
    class Meta(BaseMeta):
        tablename = "task_sheldules"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task)
    schedule = ormar.JSON()
    executors = ormar.ManyToMany(User)


class ScheduledTask(ormar.Model):
    class Meta(BaseMeta):
        tablename = "shelduled_tasks"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task)
    task_schedule: Optional[TaskSchedule] = ormar.ForeignKey(TaskSchedule)
    scheduled_to: datetime = ormar.DateTime(timezone=True)  # type: ignore


class CompletedTask(ormar.Model):
    class Meta(BaseMeta):
        tablename = "completed_tasks"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task)
    scheduled_task: Optional[ScheduledTask] = ormar.ForeignKey(
        ScheduledTask, nullable=True
    )
    complete_on: datetime = ormar.DateTime(timezone=True)  # type: ignore
    executors = ormar.ManyToMany(User)
