from fastapi import APIRouter

from app.apartments.views.apartment import apartments_router
from app.apartments.views.rooms import apartment_rooms_router, rooms_router

routers: list[APIRouter] = [
    apartments_router,
    apartment_rooms_router,
    rooms_router,
]
