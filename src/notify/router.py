from aiogram.types import Message
from aiogram3_triggers import TRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Инициализация TRouter
router = TRouter()

# Инициализация планировщика
scheduler = AsyncIOScheduler()

# Пример функции для получения книги (или можно добавить свою логику)
async def find_book_to_read():
    # Здесь нужно реализовать логику для получения книги
    book = "Твоя книга дня"  # Пример названия книги
    return book

# Функция для отправки уведомления пользователю
async def send_reminder_to_user(msg: Message,chat_id, book):
    message = f"Не забудь прочитать сегодня: {book}"
    await msg.send_message(chat_id=chat_id, text=message)

# Триггер, который будет срабатывать каждый день
@router.triggers_handler("daily")  # Время можно изменить на нужное
async def notify_to_read_book_every_day(msg, event):
    chat_id = event.chat.id  # Получение ID чата, куда отправлять уведомление
    book = await find_book_to_read()
    await send_reminder_to_user(msg, chat_id, book)

# Запуск планировщика
async def start_scheduler():
    scheduler.add_job(
        notify_to_read_book_every_day,
        trigger='cron',
        hour=13,  # Указываем время, когда будет отправляться уведомление (08:00)
    )
    scheduler.start()
    
scheduler.add_job(notify_to_read_book_every_day, 'cron', hour=13, minute=5)
scheduler.start()

