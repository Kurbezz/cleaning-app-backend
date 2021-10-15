from datetime import datetime, time
from typing import Literal, Union
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, conint, PositiveInt
from starlette.background import BackgroundTasks

from app.tasks.serializers.task import Task


class ScheduleType(str, Enum):
    days_of_the_week = "days_of_the_week"
    days_of_the_month = "days_of_the_month"
    repeat_every_n_days = "repeat_every_n_days"
    some_date = "some_date"


class WeekDays(str, Enum):
    monday = "mo"
    tuesday = "tu"
    wednesday = "we"
    thursday = "th"
    friday = "fr"
    saturday = "sa"
    sunday = "su"


class ScheduleDaysOfTheWeek(BaseModel):
    type: Literal[ScheduleType.days_of_the_week]
    week_days: list[WeekDays]
    time: time


class ScheduleDaysOfTheMonth(BaseModel):
    type: Literal[ScheduleType.days_of_the_month]
    months_days: list[conint(ge=1, le=31)]  # type: ignore
    time: time


class ScheduleRepeatEveryNDays(BaseModel):
    type: Literal[ScheduleType.repeat_every_n_days]
    days_count: PositiveInt
    time: time


class ScheduleSomeDay(BaseModel):
    type: Literal[ScheduleType.some_date]
    date: datetime


Schedules = Union[
    ScheduleDaysOfTheWeek,
    ScheduleDaysOfTheMonth,
    ScheduleRepeatEveryNDays,
    ScheduleSomeDay,
]


class TaskScheduleTask(BaseModel):
    id: int


class TaskScheduleUser(BaseModel):
    id: UUID


class TaskSchedule(BaseModel):
    id: int
    task: TaskScheduleTask
    schedule: Schedules
    executors: list[TaskScheduleUser]


class CreateSchedule(BaseModel):
    task: int
    schedule: Schedules
    executors: list[UUID]
