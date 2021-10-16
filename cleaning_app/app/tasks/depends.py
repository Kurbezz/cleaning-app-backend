from typing import Union

from fastapi import Depends, HTTPException, status

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.apartments.models import Apartment

from app.tasks.serializers.task import CreateTask, UpdateTask
from app.tasks.models import Task, TaskSchedule


async def get_apartment(
    data: CreateTask, user: User = Depends(get_current_user_obj)
):
    apartment = await Apartment.objects.get(
        id=data.apartment, users__id=user.id
    )

    if not apartment:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Bad apartment!")

    return apartment


async def get_rooms(
    data: Union[CreateTask, UpdateTask],
    apartment: Apartment = Depends(get_apartment),
):
    return await apartment.rooms.filter(id__in=data.rooms).all()


async def get_task_obj(
    task_id: int, user: User = Depends(get_current_user_obj)
):
    task = await Task.objects.get_or_none(
        id=task_id,
        apartment__users__id=user.id,
    )

    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return task


async def get_task_schedule_obj(
    task_schedule_id: int, user: User = Depends(get_current_user_obj)
):
    task_schedule = await TaskSchedule.objects.get(
        id=task_schedule_id, task__apartment__users__id=user.id
    )

    if not task_schedule:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return task_schedule
