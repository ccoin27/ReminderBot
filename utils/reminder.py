from datetime import datetime
import asyncio
from utils.database import get_due_reminders, delete_reminder

async def reminder_worker(bot):
    while True:
        now = datetime.now().isoformat()
        tasks = await get_due_reminders(now)
        for task_id, user_id, text in tasks:
            await bot.send_message(user_id, f"🔔 <b>Напоминание!</b>\n\n📌 <i>{text}</i>")
            await delete_reminder(task_id)
        await asyncio.sleep(10)
