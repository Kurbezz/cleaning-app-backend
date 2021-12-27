from fastapi import APIRouter, Depends

from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate

from app.apartments.depends.apartment import get_apartment
from app.apartments.depends.room import get_apartment_obj, get_room_obj
from app.apartments.models import Apartment as ApartmentModel
from app.apartments.models import Room as RoomModel
from app.apartments.serializers.room import (
    CreateRoomWithApartment,
    Room,
    UpdateRoom,
)
from app.common.pagination_page import CustomPage
from app.users.depends import get_current_user_obj
from app.users.models import User

apartment_rooms_router = APIRouter(
    prefix="/api/apartments/{apartment_id}/rooms", tags=["apartments"]
)


@apartment_rooms_router.get(
    "",
    response_model=CustomPage[Room],
    dependencies=[Depends(Params)],
)
async def get_all_apartment_rooms(
    apartment: ApartmentModel = Depends(get_apartment),
):
    return await paginate(apartment.rooms.select_related("tasks").queryset)


rooms_router = APIRouter(prefix="/api/rooms", tags=["rooms"])


@rooms_router.get(
    "",
    response_model=CustomPage[Room],
    dependencies=[Depends(Params)],
)
async def get_all_rooms(user: User = Depends(get_current_user_obj)):
    return await paginate(
        RoomModel.objects.filter(apartment__users__id=user.id).select_related(
            "tasks"
        )
    )


@rooms_router.post(
    "", response_model=Room, dependencies=[Depends(get_apartment_obj)]
)
async def create_room(data: CreateRoomWithApartment):
    return await RoomModel.objects.create(**data.dict())


@rooms_router.get("/{room_id}", response_model=Room)
def get_room(room: RoomModel = Depends(get_room_obj)):
    return room


@rooms_router.put("/{room_id}", response_model=Room)
async def update_room(
    data: UpdateRoom, room: RoomModel = Depends(get_room_obj)
):
    return await room.update_from_dict(data.dict()).update()


@rooms_router.delete("/{room_id}", response_model=Room)
async def delete_room(room: RoomModel = Depends(get_room_obj)):
    print("Test")

    await room.delete()

    return room
