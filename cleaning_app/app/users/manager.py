from typing import Optional

from fastapi import Depends, Request
from fastapi_users.manager import BaseUserManager
from fastapi_mail import MessageSchema

from core.config import env_config

from app.users.serializers import UserRegister, UserDB
from app.users.models import get_user_db


SECRET = env_config.SECRET


class UserManager(BaseUserManager[UserRegister, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: UserDB, request: Optional[Request] = None
    ):
        await self.request_verify(user, request)

    async def on_after_request_verify(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        html = f"""
        {env_config.SERVER_PREFIX}/verify_user?token={token}
        """

        message = MessageSchema(
            subject="Подтверждение почты",
            recipients=[user.email],
            body=html,
            subtype="html",
        )

        await request.app.state.fm.send_message(message)

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        html = f"""
        {env_config.SERVER_PREFIX}/reset_password?token={token}
        """

        message = MessageSchema(
            subject="Восстановление пароля",
            recipients=[user.email],
            body=html,
            subtype="html",
        )

        await request.app.state.fm.send_message(message)


def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    return UserManager(user_db)
