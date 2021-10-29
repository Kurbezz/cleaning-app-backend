from datetime import datetime, timedelta
from fastapi import HTTPException, status, BackgroundTasks

from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

from app.users.models import User

from app.tasks.models import (
    Task as TaskModel,
    TaskSchedule as TaskSheduleModel,
    ScheduledTask as ScheduledTaskModel,
)
from app.tasks.serializers.task_schedule import (
    WeekDays,
    CreateSchedule,
    ScheduleSomeDay,
    ScheduleDaysOfTheWeek,
    ScheduleDaysOfTheMonth,
    ScheduleRepeatEveryNDays,
)


class TaskScheduler:
    def __init__(
        self,
        task_schedule: CreateSchedule,
        task_schedule_id: int,
        task: TaskModel,
        executors: list[User],
    ):
        self.task_schedule = task_schedule
        self.task_schedule_id = task_schedule_id
        self.task = task
        self.executors = executors

    async def _create_scheduled_task(self, scheduled_to: datetime):
        await ScheduledTaskModel.objects.get_or_create(
            task=self.task.id,
            task_schedule=self.task_schedule_id,
            scheduled_to=scheduled_to,
        )

    def _get_schedule_days_of_week_relativedelta(
        self, schedule: ScheduleDaysOfTheWeek
    ) -> list[relativedelta]:
        relativedelta_weekdays = {
            WeekDays.monday: MO,
            WeekDays.tuesday: TU,
            WeekDays.wednesday: WE,
            WeekDays.thursday: TH,
            WeekDays.friday: FR,
            WeekDays.saturday: SA,
            WeekDays.sunday: SU,
        }

        return [
            relativedelta(days=1, weekday=relativedelta_weekdays[weekday])
            for weekday in schedule.week_days
        ]

    async def _schedule_days_of_month(
        self, schedule: ScheduleDaysOfTheMonth
    ) -> list[relativedelta]:
        return [
            relativedelta(month=1, day=day) for day in schedule.months_days
        ]

    async def _schedule_repeat_every_n_day(
        self, schedule: ScheduleRepeatEveryNDays
    ):
        return [relativedelta(days=schedule.days_count)]

    async def _schedule(self):
        relative_deltas: list[relativedelta] = []

        if isinstance(self.task_schedule.schedule, ScheduleSomeDay):
            await self._create_scheduled_task(self.task_schedule.schedule.date)
            return
        elif isinstance(self.task_schedule.schedule, ScheduleDaysOfTheWeek):
            relative_deltas = self._get_schedule_days_of_week_relativedelta(
                self.task_schedule.schedule
            )
        elif isinstance(self.task_schedule.schedule, ScheduleDaysOfTheMonth):
            await self._schedule_days_of_month(self.task_schedule.schedule)
        elif isinstance(self.task_schedule.schedule, ScheduleRepeatEveryNDays):
            await self._schedule_repeat_every_n_day(
                self.task_schedule.schedule
            )
        else:
            raise NotImplementedError("Schedule not implemented!")

        schedule = self.task_schedule.schedule

        for r_delta in relative_deltas:
            now = datetime.now()
            t_date = datetime.now()
            t_date.replace(
                hour=schedule.time.hour,
                minute=schedule.time.minute,
                microsecond=0,
            )

            t_date += r_delta
            while t_date - now <= timedelta(days=365):
                await self._create_scheduled_task(t_date)

    @classmethod
    async def execute(
        cls, task_schedule: CreateSchedule, task_schedule_id: int
    ):
        task = await TaskModel.objects.get(id=task_schedule.task)
        executors = await User.objects.filter(
            id__in=task_schedule.executors
        ).all()

        scheduler = TaskScheduler(
            task_schedule, task_schedule_id, task, executors
        )
        await scheduler._schedule()


async def create_task_shedule(
    data: CreateSchedule,
    user: User,
    background_task: BackgroundTasks,
) -> TaskSheduleModel:
    task = await TaskModel.objects.select_related(["apartment"]).get_or_none(
        id=data.task, apartment__users__id=user.id
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad task!"
        )

    executors = await User.objects.filter(
        id__in=data.executors, apartments__id=task.apartment.id
    ).all()

    if len(executors) != len(data.executors):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad executor ids!"
        )

    task_shedule = (
        await TaskSheduleModel.objects.select_related(["task"])
        .prefetch_related(["executors"])
        .create(
            task=task.id,
            schedule=data.schedule.json(),
        )
    )

    background_task.add_task(TaskScheduler.execute, data, task_shedule.id)

    return task_shedule
