from fastapi import APIRouter, BackgroundTasks, Depends

from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate

from app.common.pagination_page import CustomPage
from app.tasks.depends import get_task_schedule_obj
from app.tasks.models import TaskSchedule as TaskScheduleModel
from app.tasks.serializers.task_schedule import CreateSchedule, TaskSchedule
from app.tasks.services.task_schedule_create import (
    create_task_shedule as create_task_shedule_service,
)
from app.users.depends import get_current_user_obj
from app.users.models import User

task_schedules_router = APIRouter(
    prefix="/api/task_schedules", tags=["task_schedules"]
)


@task_schedules_router.get(
    "",
    response_model=CustomPage[TaskSchedule],
    dependencies=[Depends(Params)],
)
async def get_task_schedules(user: User = Depends(get_current_user_obj)):
    return await paginate(
        TaskScheduleModel.objects.select_related("executors").filter(
            task__apartment__users__id=user.id
        )
    )


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
    await task_schedule.delete()

    return task_schedule
