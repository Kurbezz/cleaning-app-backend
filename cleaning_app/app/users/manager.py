from typing import Optional

from fastapi import Depends, Request
from fastapi_users.manager import BaseUserManager

from core.config import env_config

from app.users.serializers import UserRegister, UserDB
from app.users.models import get_user_db


SECRET = env_config.SECRET


class UserManager(BaseUserManager[UserRegister, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    return UserManager(user_db)
