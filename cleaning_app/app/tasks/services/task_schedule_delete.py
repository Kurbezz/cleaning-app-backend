from datetime import datetime

from app.tasks.models import TaskSchedule, ScheduledTask


async def delete_task_schedule(task_schedule: TaskSchedule) -> TaskSchedule:
    now = datetime.now()

    await ScheduledTask.objects.filter(
        task_schedule=task_schedule.id, scheduled_to__gt=now
    ).delete()

    task_schedule.is_deleted = True
    await task_schedule.save()

    return task_schedule
