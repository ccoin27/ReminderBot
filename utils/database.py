import aiosqlite

DB_NAME = "reminders.db"
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                remind_time TEXT
            )
        """)
        await db.commit()

async def add_reminder(user_id, text, remind_time):
    if not isinstance(user_id, int):
        raise ValueError("user_id должен быть целым числом")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text должен быть непустой строкой")
    if not isinstance(remind_time, str) or not remind_time.strip():
        raise ValueError("remind_time должен быть строкой в формате ISO")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO reminders (user_id, text, remind_time) VALUES (?, ?, ?)",
            (user_id, text, remind_time)
        )
        await db.commit()

async def get_user_reminders(user_id):
    if not isinstance(user_id, int):
        raise ValueError("user_id должен быть целым числом")

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id, text, remind_time FROM reminders WHERE user_id = ? ORDER BY remind_time",
            (user_id,)
        )
        result = await cursor.fetchall()
        return result if result else []

async def delete_reminder(task_id):
    if not isinstance(task_id, int):
        raise ValueError("task_id должен быть целым числом")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM reminders WHERE id = ?", (task_id,))
        await db.commit()

async def get_due_reminders(now_iso):
    if not isinstance(now_iso, str) or not now_iso.strip():
        raise ValueError("now_iso должен быть строкой в формате ISO")

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id, user_id, text FROM reminders WHERE remind_time <= ?",
            (now_iso,)
        )
        result = await cursor.fetchall()
        return result if result else []
