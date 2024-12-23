import asyncio
from datetime import datetime, time, timedelta


async def run_daily_task(task_func, scheduled_time: time, **kwargs):
    while True:
        now = datetime.now()
        today_scheduled = datetime.combine(now.date(), scheduled_time)
        if now > today_scheduled:
            next_run = today_scheduled + timedelta(days=1)
        else:
            next_run = today_scheduled
        wait_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        await task_func(**kwargs)
        await asyncio.sleep(86400)  # Sleep for 24 hours
