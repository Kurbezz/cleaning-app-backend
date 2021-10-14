from datetime import datetime
from fastapi import Depends, HTTPException, status, BackgroundTasks

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.tasks.models import Task as TaskModel, TaskSchedule as TaskSheduleModel, ScheduledTask as ScheduledTaskModel
from app.tasks.serializers.task_schedule import CreateSchedule, ScheduleSomeDay, ScheduleDaysOfTheWeek


async def schedule_tasks(task_schedule: CreateSchedule, task_schedule_id: int):
    task = await TaskModel.objects.get(id=task_schedule.task)
    executors = await User.objects.filter(id__in=task_schedule.executors).all()

    async def create_scheduled_task(scheduled_to: datetime):
        schedule_task = await ScheduledTaskModel.objects.create(
            task=task.id,
            task_schedule=task_schedule_id,
            scheduled_to=scheduled_to
        )

        for executor in executors:
            schedule_task.executors.add(executor)

    if isinstance(task_schedule.schedule, ScheduleSomeDay):
        await create_scheduled_task(task_schedule.schedule.date)
    elif isinstance(task_schedule.schedule, ScheduleDaysOfTheWeek):
        pass


async def create_task_shedule(data: CreateSchedule, user: User = Depends(get_current_user_obj)) -> TaskSheduleModel:
    task = await TaskModel.objects \
        .select_related(["apartment"]) \
        .get_or_none(id=data.task, apartment__users__id=user.id)

    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad task!")

    executors = await User.objects.filter(id__in=data.executors, apartments__id=task.apartment.id).all()

    if len(executors) != len(data.executors):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad executor ids!")

    task_shedule = await TaskSheduleModel.objects.create(
        task=task,
        schedule=data.sheldule,
    )

    for executor in executors:
        task_shedule.executors.add(executor)

    BackgroundTasks.add_task(schedule_tasks, data, task_shedule.id)

    return task_shedule
