from fastapi import APIRouter

from app.users.views import router as users_router
from app.apartments.routers import routers as appartments_routers
from app.tasks.views import tasks_router, task_schedules_router, scheduled_tasks_routers


routers: list[APIRouter] = [
    users_router,
    *appartments_routers,
    tasks_router,
    task_schedules_router,
    scheduled_tasks_routers,
]
