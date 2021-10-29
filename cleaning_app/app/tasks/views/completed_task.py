from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.common.pagination_page import CustomPage
from fastapi_pagination import LimitOffsetParams
from fastapi_pagination.ext.ormar import paginate

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.tasks.models import (
    CompletedTask as CompletedTaskModel,
    Task as TaskModel,
)
from app.tasks.serializers.completed_task import CompletedTask
from app.tasks.depends import get_task_obj


completed_tasks_router = APIRouter(
    prefix="/api/completed_tasks", tags=["completed_tasks"]
)


@completed_tasks_router.get(
    "",
    response_model=CustomPage[CompletedTask],
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


task_complete_router = APIRouter(tags=["tasks"])


@task_complete_router.post(
    "/api/tasks/{task_id}/complete", response_model=CompletedTask
)
async def complete_task(
    task: TaskModel = Depends(get_task_obj),
    user: User = Depends(get_current_user_obj),
):
    completed_task = await CompletedTaskModel.objects.create(
        task=task.id,
        complete_on=datetime.now(),
    )

    await completed_task.executors.add(user)

    return completed_task
