from typing import Optional

import ormar
from ormar import property_field

from core.db import BaseMeta
from app.users.models import User


class Apartment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "apartments"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    name: str = ormar.String(max_length=32)  # type: ignore
    users = ormar.ManyToMany(User)


class Room(ormar.Model):
    class Meta(BaseMeta):
        tablename = "rooms"

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    name: str = ormar.String(max_length=32)  # type: ignore
    apartment: Apartment = ormar.ForeignKey(Apartment, ondelete="CASCADE")
    color: Optional[str] = ormar.String(
        max_length=6, nullable=True
    )  # type: ignore

    @property_field
    def tasks_count(self) -> int:
        return len(self.tasks)
