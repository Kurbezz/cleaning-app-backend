from datetime import datetime

import ormar

from core.db import BaseMeta
from app.apartments.models import Apartment, Room
from app.users.models import User


class Task(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'tasks'

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    name: str = ormar.String(max_length=32)  # type: ignore
    description: str = ormar.String(max_length=128)  # type: ignore
    apartment: Apartment = ormar.ForeignKey(Apartment)
    rooms: list[Room] = ormar.ManyToMany(Room)


class TaskSchedule(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'task_sheldules'

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task)
    schedule = ormar.JSON()
    executors: list[User] = ormar.ManyToMany(User)


class ScheduledTask(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'shelduled_tasks'

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task)
    task_schedule: TaskSchedule = ormar.ForeignKey(TaskSchedule)
    scheduled_to: datetime = ormar.DateTime(timezone=True)  # type: ignore


class CompletedTask(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'completed_tasks'

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    task: Task = ormar.ForeignKey(Task)
    scheduled_task: ScheduledTask = ormar.ForeignKey(ScheduledTask)
    complete_on: datetime = ormar.DateTime(timezone=True)  # type: ignore
    executors: list[User] = ormar.ManyToMany(User)
