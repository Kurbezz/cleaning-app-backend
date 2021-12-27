from typing import Optional

from pydantic import BaseModel, constr


class RoomApartment(BaseModel):
    id: int


class Room(BaseModel):
    id: int
    name: str
    apartment: RoomApartment
    color: Optional[str]
    tasks_count: int


class CreateRoom(BaseModel):
    name: constr(max_length=32)  # type: ignore
    color: Optional[constr(max_length=6)]  # type: ignore


class CreateRoomWithApartment(CreateRoom):
    apartment: int


class UpdateRoom(BaseModel):
    name: constr(max_length=32)  # type: ignore
    color: Optional[constr(max_length=6)]  # type: ignore
