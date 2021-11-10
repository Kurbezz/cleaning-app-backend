from fastapi import FastAPI

from fastapi_pagination import add_pagination

from fastapi_mail import FastMail, ConnectionConfig

from core.db import database
from core.config import env_config
from app.routers import routers
from app.users.router import init_auth_routes


def start_app() -> FastAPI:
    app = FastAPI()

    app.state.database = database

    app.state.fm = FastMail(
        ConnectionConfig(
            MAIL_USERNAME=env_config.MAIL_USERNAME,
            MAIL_PASSWORD=env_config.MAIL_PASSWORD,
            MAIL_FROM=env_config.MAIL_FROM,
            MAIL_PORT=env_config.MAIL_PORT,
            MAIL_SERVER=env_config.MAIL_SERVER,
            MAIL_TLS=env_config.MAIL_TLS,
            MAIL_SSL=env_config.MAIL_SSL,
            USE_CREDENTIALS=env_config.USE_CREDENTIALS,
            VALIDATE_CERTS=env_config.VALIDATE_CERTS,
        )
    )

    init_auth_routes(app)

    for router in routers:
        app.include_router(router)

    add_pagination(app)

    @app.on_event("startup")
    async def startup() -> None:
        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()

    return app
