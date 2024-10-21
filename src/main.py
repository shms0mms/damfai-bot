import datetime
import logging
from uuid import uuid4
import bcrypt
from sqlalchemy import select
from auth.models import  User, UserTg
import asyncio
from books.models import Book
from middleware.db import SessionMiddleware
from support.router import router as support_router
from auth.router import router as auth_router
from books.router import router as books_router
from aiogram import Bot, Dispatcher, Router
from db import session
from aiogram.filters import Command
from aiogram import types
from markups import auth_user_markup, user_markup
from sqlalchemy.ext.asyncio import AsyncSession
from config import config
from db import create_db
from aiogram import Bot, Dispatcher
from aiogram3_triggers import TRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.util import utc
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
user_data = {}
bot = Bot(config.env.TOKEN)
dp = Dispatcher()  

dp.update.middleware(SessionMiddleware(session_pool=session))
router = Router(name="main")
@router.message(Command('start'))
async def start(msg: types.Message, session: AsyncSession):
    text = rf'Приветствуем в damfai, {msg.from_user.mention_html()}!'
    tg_id = msg.from_user.id
    start_user = User(
    name="Александр",
    surname="Шаронов",
    email="shmsmms01@gmail.com",
    # id=uuid4(),
    password=bcrypt.hashpw(password='12345678'.encode(), salt=bcrypt.gensalt()),
    dob=datetime.datetime.now().date()
    )
    start_book1 = Book(
    title="Идиот",
    author="Федор Достоевский",
    desc="Идиот - книга о князе, который променял жену на любовницу",
    writen_date=datetime.date.today(),
    age_of_book=1
)   
    start_book2 = Book(
    title="Олег",
    author="Федор Достоевский",
    desc="Идиот - книга о князе, который променял жену на любовницу",
    writen_date=datetime.date.today(),
    age_of_book=2
)   
    session.add(start_book1)
    session.add(start_book2)
    session.add(start_user)
    await session.flush()
    statement = select(UserTg).where(UserTg.tg_id == tg_id)
    user_tg = await session.execute(statement)
    user_tg = user_tg.scalar_one_or_none()

    await session.commit()
    markup = None
    if user_tg is None:
        markup = user_markup
    else:
        markup = auth_user_markup
    user_data['chat_id'] = msg.chat.id 
    await start_scheduler(msg, bot)
    
    await msg.answer(text=text, reply_markup=markup, parse_mode='HTML')



notify_router = TRouter()

scheduler = AsyncIOScheduler()
scheduler.configure(timezone=utc)
async def find_book_to_read():
    book = 'Твоя книга дня 📚 - "Идиот", Достоевский А.А.'  # Пример названия книги
    return book

# Функция для отправки уведомления пользователю
async def send_reminder_to_user(chat_id: int, bot: Bot):
    book = await find_book_to_read()
    message = f"Не забудь прочитать сегодня: {book}"
    await bot.send_message(chat_id=chat_id, text=message)

# Триггер, который будет срабатывать каждый день
@notify_router.triggers_handler('minute')
async def notify_to_read_book_every_day(dp: Dispatcher, bot: Bot):
    if 'chat_id' in user_data and user_data['chat_id']:
        await send_reminder_to_user(user_data["chat_id"], bot)

# Запуск планировщика
async def start_scheduler(dp: Dispatcher, bot: Bot):
    scheduler.add_job(
        send_reminder_to_user,
        trigger='cron',
        hour=22,
        minute=21,
        kwargs={"chat_id": dp.chat.id, "bot": bot }
    )
    scheduler.start()
    




async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    await create_db()
    dp.include_router(router)
    dp.include_router(auth_router)
    dp.include_router(support_router)
    dp.include_router(notify_router)
    dp.include_router(books_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
