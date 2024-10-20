from aiogram import Bot, Dispatcher
from aiogram3_triggers import TRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.util import utc
# Инициализация TRouter
router = TRouter()

# Инициализация планировщика
scheduler = AsyncIOScheduler()
scheduler.configure(timezone=utc)
# Пример функции для получения книги (или можно добавить свою логику)
async def find_book_to_read():
    # Здесь нужно реализовать логику для получения книги
    book = "Твоя книга дня"  # Пример названия книги
    return book

# Функция для отправки уведомления пользователю
async def send_reminder_to_user(chat_id: int, bot: Bot):
    book = await find_book_to_read()
    message = f"Не забудь прочитать сегодня: {book}"
    await bot.send_message(chat_id=chat_id, text=message)

# Триггер, который будет срабатывать каждый день
@router.triggers_handler('minute')
async def notify_to_read_book_every_day(dp: Dispatcher, bot: Bot):
    await send_reminder_to_user(user_data["chat_id"], bot)

# Запуск планировщика
async def start_scheduler(dp: Dispatcher, bot: Bot):
    scheduler.add_job(
        send_reminder_to_user,
        trigger='cron',
        hour=22,
        minute=17,
        kwargs={"chat_id": dp.chat.id, "bot": bot }
    )
    scheduler.start()
    

