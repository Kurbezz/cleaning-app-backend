from fastapi import APIRouter, Depends

from fastapi_pagination import LimitOffsetPage, LimitOffsetParams
from fastapi_pagination.ext.ormar import paginate

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.tasks.serializers.scheduled_task import ScheduledTask
from app.tasks.models import ScheduledTask as ScheduledTaskModel


scheduled_tasks_router = APIRouter(prefix="/api/scheduled_tasks", tags=["scheduled_tasks"])


@scheduled_tasks_router.get("", response_model=LimitOffsetPage[ScheduledTask], dependencies=[Depends(LimitOffsetParams)])
async def get_scheduled_task(user: User = Depends(get_current_user_obj)):
    return await paginate(ScheduledTaskModel.objects.filter(
        task__apartment__users__id=user.id
    ))
