from fastapi import FastAPI

from core.db import database
from app.routers import routers
from app.users.router import init_auth_routes


def start_app() -> FastAPI:
    app = FastAPI()

    app.state.database = database

    init_auth_routes(app)

    for router in routers:
        app.include_router(router)

    @app.on_event('startup')
    async def startup() -> None:
        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    @app.on_event('shutdown')
    async def shutdown() -> None:
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()

    return app
