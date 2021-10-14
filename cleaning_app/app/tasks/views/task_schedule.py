from fastapi import APIRouter, Depends

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.tasks.models import TaskSchedule as TaskScheduleModel
from app.tasks.serializers.task_schedule import TaskSchedule


task_schedules_router = APIRouter(
    prefix="/api/task_schedules",
    tags=["task_schedules"]
)


@task_schedules_router.get("", response_model=list[TaskSchedule])
async def get_task_schedules(user: User = Depends(get_current_user_obj)):
    return await TaskScheduleModel.objects.filter(
        task__apartment__user__id=user.id
    ).all()


@task_schedules_router.get("", response_model=TaskSchedule)
async def create_task_schedule():
    pass
