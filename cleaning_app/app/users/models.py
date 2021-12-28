import ormar

from fastapi_users_db_ormar import OrmarBaseUserModel, OrmarUserDatabase

from app.users.serializers import UserDB
from core.db import BaseMeta


class User(OrmarBaseUserModel):
    class Meta(BaseMeta):
        tablename = "users"

    name: str = ormar.String(max_length=32)  # type: ignore


def get_user_db():
    yield OrmarUserDatabase(UserDB, User)
