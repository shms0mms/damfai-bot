import logging
from uuid import uuid4
import bcrypt
from sqlalchemy import select
from auth.models import  User, UserTg
from config import TOKEN
import asyncio
from middleware.db import SessionMiddleware
from support.support import router as support_router
from auth.router import router as auth_router
from aiogram import Bot, Dispatcher, Router
from db import session
from aiogram.filters import Command
from aiogram import types
from markups import auth_user_markup, user_markup
from sqlalchemy.ext.asyncio import AsyncSession
from notify.router import router as notify_router
bot = Bot(TOKEN)
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
    id=uuid4(),
    password=bcrypt.hashpw(password='12345678'.encode(), salt=bcrypt.gensalt())
)
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
    await msg.answer(text=text, reply_markup=markup, parse_mode='HTML')


from config import TOKEN
from db import create_db
async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    await create_db()
    dp.include_router(router)
    dp.include_router(auth_router)
    dp.include_router(support_router)
    dp.include_router(notify_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
