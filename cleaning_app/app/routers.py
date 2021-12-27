from fastapi import APIRouter

from app.apartments.routers import routers as appartments_routers
from app.tasks.views import (
    completed_tasks_router,
    scheduled_tasks_router,
    task_complete_router,
    task_schedules_router,
    tasks_router,
)
from app.users.views import router as users_router

routers: list[APIRouter] = [
    users_router,
    *appartments_routers,
    tasks_router,
    task_schedules_router,
    scheduled_tasks_router,
    completed_tasks_router,
    task_complete_router,
]
