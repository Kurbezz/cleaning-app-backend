from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    id: int


class TaskSchedule(BaseModel):
    id: int


class ScheduledTask(BaseModel):
    id: int
    task: Task
    task_schedule: TaskSchedule
    scheduled_to: datetime
