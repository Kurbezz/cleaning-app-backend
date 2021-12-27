import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    name: str


class ApartmentRoom(BaseModel):
    id: int
    name: str
    color: Optional[str]
    tasks_count: int


class Apartment(BaseModel):
    id: int
    name: str
    users: list[User]
    rooms: list[ApartmentRoom]


class CreateApartment(BaseModel):
    name: constr(max_length=32)  # type: ignore


class UpdateApartment(BaseModel):
    name: constr(max_length=32)  # type: ignore
