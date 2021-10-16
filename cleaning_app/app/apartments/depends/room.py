from fastapi import Depends, HTTPException, status

from app.users.models import User
from app.users.depends import get_current_user_obj

from app.apartments.depends.apartment import get_apartment
from app.apartments.models import Apartment, Room
from app.apartments.serializers.room import CreateRoomWithApartment


async def get_room_in_apartment(
    room_id: int, apartment: Apartment = Depends(get_apartment)
):
    room = apartment.rooms.get_or_none(id=room_id)

    if not room:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return room


async def get_apartment_obj(
    data: CreateRoomWithApartment, user: User = Depends(get_current_user_obj)
):
    apartment = await user.apartments.get_or_none(id=data.apartment)

    if not apartment:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Bad apartment!")

    return apartment


async def get_room_obj(
    room_id: int, user: User = Depends(get_current_user_obj)
):
    room = Room.objects.get(id=room_id, apartment__users__id=user.id)

    if not room:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return room
