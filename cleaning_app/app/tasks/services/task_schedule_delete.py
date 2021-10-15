from datetime import datetime

from app.tasks.models import TaskSchedule, ScheduledTask


async def delete_task_schedule(task_schedule: TaskSchedule):
    now = datetime.now()

    await ScheduledTask.objects.filter(
        task_schedule=task_schedule.id, scheduled_to__gt=now
    ).delete()

    await ScheduledTask.objects.filter(
        task_schedule=task_schedule.id, scheduled_to__lte=now
    ).update(task_schedule=None)

    await task_schedule.delete()
