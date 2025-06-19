from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я твой бот-напоминалка.\n\n"
        "📌 Команды:\n"
        "➕ <b>/add</b> — создать напоминание\n"
        "📃 <b>/list</b> — список задач\n"
        "Начнём?"
    )