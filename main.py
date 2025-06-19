import asyncio, json, logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from utils import database, reminder
from handlers import start, add, list

bot = Bot(token=json.load(open("config.json"))["BOT_TOKEN"], default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

dp.include_routers( 
    start.router,
    add.router,
    list.router
)

async def main():
    await database.init_db()
    asyncio.create_task(reminder.reminder_worker(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
