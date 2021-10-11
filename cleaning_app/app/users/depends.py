from fastapi import Depends

from app.users.serializers import UserDB
from app.users.router import fastapi_users
from app.users.models import User


get_current_active_user = fastapi_users.authenticator.current_user(active=True)
get_current_superuser = fastapi_users.authenticator.current_user(active=True, superuser=True)


async def get_current_user_obj(user_db: UserDB = Depends(get_current_active_user)):
    return await User.objects.get(id=user_db.id)
