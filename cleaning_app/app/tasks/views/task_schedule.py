from fastapi import APIRouter, Depends, BackgroundTasks

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.tasks.models import TaskSchedule as TaskScheduleModel
from app.tasks.serializers.task_schedule import TaskSchedule, CreateSchedule
from app.tasks.services.task_schedule_create import (
    create_task_shedule as create_task_shedule_service,
)
from app.tasks.services.task_schedule_delete import (
    delete_task_schedule as delete_task_schedule_service,
)
from app.tasks.depends import get_task_schedule_obj


task_schedules_router = APIRouter(prefix="/api/task_schedules", tags=["task_schedules"])


@task_schedules_router.get("", response_model=list[TaskSchedule])
async def get_task_schedules(user: User = Depends(get_current_user_obj)):
    return await TaskScheduleModel.objects.filter(
        task__apartment__users__id=user.id
    ).all()


@task_schedules_router.post(
    "",
    response_model=TaskSchedule,
)
async def create_task_schedule(
    data: CreateSchedule,
    background_task: BackgroundTasks,
    user: User = Depends(get_current_user_obj),
):
    return await create_task_shedule_service(data, user, background_task)


@task_schedules_router.get(
    "/{task_schedule_id}",
    response_model=TaskSchedule,
)
async def get_task_schedule(
    task_schedule: TaskScheduleModel = Depends(get_task_schedule_obj),
):
    return task_schedule


@task_schedules_router.delete(
    "/{task_schedule_id}",
    response_model=TaskSchedule,
)
async def delete_task_schedule(
    task_schedule: TaskScheduleModel = Depends(get_task_schedule_obj),
):
    await delete_task_schedule_service(task_schedule)
    return task_schedule
