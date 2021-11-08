from fastapi import APIRouter, Depends, HTTPException, status

from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate
from app.common.pagination_page import CustomPage

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.tasks.serializers.scheduled_task import ScheduledTask
from app.tasks.models import ScheduledTask as ScheduledTaskModel


scheduled_tasks_router = APIRouter(
    prefix="/api/scheduled_tasks", tags=["scheduled_tasks"]
)


@scheduled_tasks_router.get(
    "",
    response_model=CustomPage[ScheduledTask],
    dependencies=[Depends(Params)],
)
async def get_scheduled_tasks(user: User = Depends(get_current_user_obj)):
    return await paginate(
        ScheduledTaskModel.objects.filter(task__apartment__users__id=user.id)
    )


@scheduled_tasks_router.get(
    "/{scheduled_task_id}",
    response_model=ScheduledTask,
)
async def get_scheduled_task(
    scheduled_task_id: int, user: User = Depends(get_current_user_obj)
):
    scheduled_task = await ScheduledTaskModel.objects.get_or_none(
        id=scheduled_task_id, task__apartment__users__id=user.id
    )

    if not scheduled_task:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return scheduled_task
