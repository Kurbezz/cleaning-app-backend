from fastapi import APIRouter, Depends

from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate

from app.apartments.models import Room
from app.common.pagination_page import CustomPage
from app.tasks.depends import get_rooms, get_task_obj
from app.tasks.models import Task as TaskModel
from app.tasks.serializers.task import CreateTask, Task, UpdateTask
from app.users.depends import get_current_user_obj
from app.users.models import User

tasks_router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@tasks_router.get(
    "",
    response_model=CustomPage[Task],
    dependencies=[Depends(Params)],
)
async def get_tasks(user: User = Depends(get_current_user_obj)):
    return await paginate(
        TaskModel.objects.select_related("rooms").filter(
            apartment__users__id=user.id
        )
    )


@tasks_router.post("", response_model=Task)
async def create_task(
    data: CreateTask, rooms: list[Room] = Depends(get_rooms)
):
    task = await TaskModel.objects.create(
        is_archived=False,
        **data.dict(),
    )

    for room in rooms:
        await task.rooms.add(room)

    return await task.update()


@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task: TaskModel = Depends(get_task_obj)):
    return task


@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(
    data: UpdateTask,
    task: TaskModel = Depends(get_task_obj),
    rooms: list[Room] = Depends(get_rooms),
):
    await task.update_from_dict(data.dict()).update()

    task.rooms.clear()
    for room in rooms:
        await task.rooms.add(room)

    return await task.update()


@tasks_router.delete("/{task_id}", response_model=Task)
async def delete_task(task: TaskModel = Depends(get_task_obj)):
    await task.delete()

    return task
