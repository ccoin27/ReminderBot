
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

def date_buttons():
    now = datetime.now()
    today_time = now + timedelta(hours=12 if (now + timedelta(hours=12)).day == now.day else 4)
    tomorrow = now + timedelta(days=1)
    kb = InlineKeyboardBuilder()
    kb.button(text="📅 Сегодня", callback_data=f"date:{today_time.strftime('%d.%m %H:%M')}")
    kb.button(text="📆 Завтра", callback_data=f"date:{tomorrow.strftime('%d.%m')} 09:00")
    kb.button(text="✏️ Ввести вручную", callback_data="custom_date")
    return kb.as_markup()
