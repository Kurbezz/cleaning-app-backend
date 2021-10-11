from fastapi import FastAPI
from fastapi_users.fastapi_users import FastAPIUsers
from fastapi_users.authentication.jwt import JWTAuthentication
    
from core.config import env_config

from app.users.serializers import User, UserRegister, UserUpdate, UserDB
from app.users.manager import get_user_manager


SECRET = env_config.SECRET

jwt_authentication = JWTAuthentication[UserRegister, UserDB](secret=SECRET, lifetime_seconds=3600)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    User,
    UserRegister,
    UserUpdate,
    UserDB,
)

def init_auth_routes(app: FastAPI):
    app.include_router(
        fastapi_users.get_auth_router(jwt_authentication),
        prefix='/auth/jwt',
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(),
        prefix="/auth",
        tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_verify_router(),
        prefix="/auth",
        tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"]
    )
