from typing import Optional
from pydantic import BaseModel, constr


class RoomApartment(BaseModel):
    id: int


class Room(BaseModel):
    id: int
    name: str
    apartment: RoomApartment
    color: Optional[str]


class CreateRoom(BaseModel):
    name: str
    color: Optional[constr(max_length=6)]  # type: ignore


class CreateRoomWithApartment(CreateRoom):
    apartment: int


class UpdateRoom(BaseModel):
    name: str
    color: Optional[constr(max_length=6)]  # type: ignore
