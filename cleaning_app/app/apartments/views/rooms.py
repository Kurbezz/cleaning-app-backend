from fastapi import APIRouter, Depends

from app.users.depends import get_current_user_obj
from app.users.models import User

from app.apartments.models import Apartment as ApartmentModel, Room as RoomModel
from app.apartments.serializers.room import Room, CreateRoom, UpdateRoom
from app.apartments.depends.apartment import get_apartment
from app.apartments.depends.room import get_room_in_apartment, get_room_obj, get_apartment_obj
from app.apartments.serializers.room import CreateRoomWithApartment


apartment_rooms_router = APIRouter(
    prefix="/api/apartments/{apartment_id}/rooms",
    tags=["rooms"]
)


@apartment_rooms_router.get("/", response_model=list[Room])
async def get_all_apartment_rooms(apartment: ApartmentModel = Depends(get_apartment)):
    return await apartment.rooms.all()


@apartment_rooms_router.post("/", response_model=Room)
async def create_apartment_room(data: CreateRoom, apartment: ApartmentModel = Depends(get_apartment)):
    return await RoomModel.objects.create(**data.dict(), apartment=apartment)


@apartment_rooms_router.get("/{room_id}", response_model=Room)
async def get_apartment_room(room: RoomModel = Depends(get_room_in_apartment)):
    return room


@apartment_rooms_router.put("/{room_id}", response_model=Room)
async def update_apartment_room(data: UpdateRoom, room: RoomModel = Depends(get_room_in_apartment)):
    return await room.update_from_dict(data.dict()).update()


@apartment_rooms_router.delete("/{room_id}", response_model=Room)
async def delete_apartment_room(room: RoomModel = Depends(get_room_in_apartment)):
    await room.delete()

    return room


rooms_router = APIRouter(
    prefix="/api/rooms",
    tags=["rooms"]
)


@rooms_router.get("", response_model=list[Room])
async def get_all_rooms(user: User = Depends(get_current_user_obj)):
    return await RoomModel.objects.filter(
        apartment__users__id=user.id
    ).all()


@rooms_router.post("", response_model=Room, dependencies=[Depends(get_apartment_obj)])
async def create_room(data: CreateRoomWithApartment):
    return await RoomModel.objects.create(**data.dict())


@rooms_router.get("/{room_id}", response_model=Room)
def get_room(room: RoomModel = Depends(get_room_obj)):
    return room


@rooms_router.put("/{room_id}", response_model=Room)
async def update_room(data: UpdateRoom, room: RoomModel = Depends(get_room_obj)):
    return await room.update_from_dict(data.dict()).update()


@rooms_router.delete("/{room_id}", response_model=Room)
async def delete_room(room: RoomModel = Depends(get_room_obj)):
    await room.delete()

    return room
