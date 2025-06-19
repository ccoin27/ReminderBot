from aiogram import Router, types
from aiogram.filters import Command
from utils.database import get_user_reminders
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

router = Router()

@router.message(Command("list"))
async def list_tasks(message: types.Message):
    try:
        await message.answer("🕒 Начинаю вывод списка задач...")
        tasks = await get_user_reminders(message.from_user.id)
        logging.info(f"User {message.from_user.id} requested list, found tasks: {tasks}")

        if not tasks:
            await message.answer("🫥 У вас пока нет задач.")
            return

        for task_id, text, time_str in tasks:
            try:
                dt = datetime.fromisoformat(time_str)
            except Exception as e:
                logging.error(f"Ошибка при разборе даты '{time_str}' для задачи {task_id}: {e}")
                dt = None

            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Выполнено", callback_data=f"done:{task_id}")]
            ])

            date_str = dt.strftime('%d.%m %H:%M') if dt else "Неизвестное время"
            await message.answer(
                f"🕒 <b>{date_str}</b>\n\n📌 <i>{text}</i>",
                reply_markup=kb
            )

    except Exception as e:
        logging.error(f"Ошибка в list_tasks: {e}")
        await message.answer("❌ Произошла ошибка при получении списка задач.")
