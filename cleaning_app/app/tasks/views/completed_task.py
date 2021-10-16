from fastapi import APIRouter, Depends, HTTPException, status

from fastapi_pagination import LimitOffsetPage, LimitOffsetParams
from fastapi_pagination.ext.ormar import paginate

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.tasks.models import CompletedTask as CompletedTaskModel
from app.tasks.serializers.completed_task import CompletedTask


completed_tasks_router = APIRouter(
    prefix="/api/completed_tasks", tags=["completed_tasks"]
)


@completed_tasks_router.get(
    "",
    response_model=LimitOffsetPage[CompletedTask],
    dependencies=[Depends(LimitOffsetParams)],
)
async def get_completed_tasks(user: User = Depends(get_current_user_obj)):
    return await paginate(
        CompletedTaskModel.objects.filter(task__apartment__users__id=user.id)
    )


@completed_tasks_router.get(
    "/{completed_task_id}", response_model=CompletedTask
)
async def get_completed_task(
    completed_task_id: int, user: User = Depends(get_current_user_obj)
):
    completed_task = await CompletedTaskModel.objects.get_or_none(
        task__apartment__users__id=user.id, task=completed_task_id
    )

    if not completed_task:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return completed_task
