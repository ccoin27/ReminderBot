from aiogram import Router, types, F
from aiogram.filters import Command
from dateutil import parser
from keyboards.date_buttons import date_buttons
from utils.database import add_reminder

router = Router()
user_states = {}

@router.message(Command("add"))
async def add(message: types.Message):
    user_states[message.from_user.id] = {}
    sent = await message.answer("🕐 Когда напомнить?", reply_markup=date_buttons())
    user_states[message.from_user.id]["last_bot_msg_id"] = sent.message_id
    user_states[message.from_user.id]["chat_id"] = message.chat.id

@router.callback_query(F.data.startswith("date:"))
async def set_date(callback: types.CallbackQuery):
    last_msg_id = user_states.get(callback.from_user.id, {}).get("last_bot_msg_id")
    chat_id = callback.message.chat.id
    if last_msg_id:
        try:
            await callback.bot.delete_message(chat_id=chat_id, message_id=last_msg_id)
        except Exception:
            pass
    user_states[callback.from_user.id]["datetime"] = callback.data[5:]
    sent = await callback.message.answer("✏️ Отлично! Теперь напиши текст задачи:")
    user_states[callback.from_user.id]["last_bot_msg_id"] = sent.message_id
    await callback.answer()

@router.callback_query(F.data == "custom_date")
async def ask_custom_date(callback: types.CallbackQuery):
    last_msg_id = user_states.get(callback.from_user.id, {}).get("last_bot_msg_id")
    chat_id = callback.message.chat.id
    if last_msg_id:
        try:
            await callback.bot.delete_message(chat_id=chat_id, message_id=last_msg_id)
        except Exception:
            pass
    sent = await callback.message.answer("📝 Введите дату и время в формате <b>25.06 14:00</b>")
    user_states[callback.from_user.id]["last_bot_msg_id"] = sent.message_id
    await callback.answer()

@router.message(F.text.regexp(r"\d{1,2}\.\d{1,2}( \d{1,2}:\d{2})?"))
async def manual_date(message: types.Message):
    state = user_states.get(message.from_user.id, {})
    last_msg_id = state.get("last_bot_msg_id")
    chat_id = message.chat.id
    if last_msg_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=last_msg_id)
        except Exception:
            pass
    user_states[message.from_user.id] = {"datetime": message.text, "chat_id": chat_id}
    sent = await message.answer("✏️ Теперь введите текст задачи:")
    user_states[message.from_user.id]["last_bot_msg_id"] = sent.message_id

@router.message(lambda message: user_states.get(message.from_user.id) is not None)
async def save_task(message: types.Message):
    state = user_states.get(message.from_user.id)
    if not state or "datetime" not in state:
        return
    try:
        dt = parser.parse(state["datetime"], dayfirst=True)
    except Exception:
        await message.answer("⚠️ Неверный формат. Пример: <b>25.06 14:00</b>")
        return
    last_msg_id = state.get("last_bot_msg_id")
    chat_id = state.get("chat_id")
    if last_msg_id and chat_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=last_msg_id)
        except Exception:
            pass
    await add_reminder(message.from_user.id, message.text, dt.isoformat())
    confirmation_text = f"✅ Готово! Напомню <b>{dt.strftime('%d.%m %H:%M')}</b>:\n\n📌 <i>{message.text}</i>"
    await message.answer(confirmation_text, parse_mode="HTML")
    user_states.pop(message.from_user.id, None)
