from pydantic import BaseModel

from datetime import datetime


class Task(BaseModel):
    id: int


class ScheduledTask(BaseModel):
    id: int


class User(BaseModel):
    id: int


class CompletedTask(BaseModel):
    id: int
    task: Task
    scheduled_task: ScheduledTask
    complete_on: datetime
    executors: list[User]
