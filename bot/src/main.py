import logging
import sys
# Imports WORKING!
sys.path.append('/app')

# for working relations
from bot.src.utils.get_markup import get_markup
from server.src.bookmarks.bookmarsk_models import FavouriteUser, BookmarkUser
from server.src.themes.themes_models import Theme
from server.src.books.books_models import Book, PageModel
from server.src.analytics.analytics_models import PagesPerDay, MinutesPerDay
from server.src.books_to_reading.booksRead_models import Reading_Book
from server.src.app_auth.auth_models import User, UserTg


import datetime
import bcrypt
from sqlalchemy import select
import asyncio
from middleware.db import SessionMiddleware
from support.router import router as support_router
from auth.router import router as auth_router
from books.router import router as books_router
from analytics.router import router as analytics_router
from aiogram import Bot, Dispatcher, Router
from server.src.db import session
from aiogram.filters import Command
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from config import config
from aiogram import Bot, Dispatcher
from aiogram3_triggers import TRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.util import utc
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


user_data = {}
bot = Bot(config.env.BOT_TOKEN)
dp = Dispatcher()  

dp.update.middleware(SessionMiddleware(session_pool=session))
router = Router(name="main")
@router.message(Command('start'))
async def start(msg: types.Message, session: AsyncSession):
    text = rf'Приветствуем в damfai, {msg.from_user.mention_html()}!'
    tg_id = msg.from_user.id
    user = User(
    name="Александр",
    surname="Шаронов",
    email="shmsmms01@gmail.com",
    password=bcrypt.hashpw(password='12345678'.encode(), salt=bcrypt.gensalt()),
    dob=datetime.datetime.now().date(),

    )
    book1 = Book(
    title="Идиот",
    author="Федор Достоевский",
    desc="Идиот - книга о князе, который променял жену на любовницу",
    writen_date=datetime.date.today(),
    age_of_book=1
)   
    book2 = Book(
    title="Олег",
    author="Федор Достоевский",
    desc="Идиот - книга о князе, который променял жену на любовницу",
    writen_date=datetime.date.today(),
    age_of_book=2
)   
    # session.add(book1)
    # session.add(book2)
    user_exists = await session.scalar(select(User).where(User.email == 'shmsmms01@gmail.com'))
    if user_exists is None:
        session.add(user)
        
    await session.flush()

    await session.commit()
    markup = await get_markup(tg_id, session)
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
@notify_router.triggers_handler('day')
async def notify_to_read_book_every_day(dp: Dispatcher, bot: Bot):
    if 'chat_id' in user_data and user_data['chat_id']:
        await send_reminder_to_user(user_data["chat_id"], bot)

# Запуск планировщика
async def start_scheduler(dp: Dispatcher, bot: Bot):
    scheduler.add_job(
        send_reminder_to_user,
        trigger='cron',
        hour=12,
        minute=0,
        kwargs={"chat_id": dp.chat.id, "bot": bot }
    )
    scheduler.start()
    




async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    dp.include_router(router)
    dp.include_router(auth_router)
    dp.include_router(support_router)
    dp.include_router(notify_router)
    dp.include_router(books_router)
    dp.include_router(analytics_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
