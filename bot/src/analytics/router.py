import datetime
import io
import logging
from const import analytics_markups
from aiogram import F, Router, types
from sqlalchemy import select
from server.src.analytics.analytics_models import MinutesPerDay
from server.src.books_to_reading.booksRead_models import Reading_Book
from server.src.app_auth.auth_models import User, UserTg
from const import markups
from sqlalchemy.ext.asyncio import AsyncSession
from server.src.utils.date import dates, monthes
from sqlalchemy.orm import selectinload
import matplotlib.pyplot as plt
from aiogram.types import BufferedInputFile, CallbackQuery
from server.src.utils.get_statistics import get_statistics
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from markups import analytics_markup
class ChooseGraphState(StatesGroup):
    choose = State()
router = Router()


@router.message(F.text == markups['statistics'])
async def statistics_handler(msg: types.Message, session: AsyncSession ):

    user = await session.scalar(
    select(User)
    .join(UserTg, User.id == UserTg.user_id)
    .where(UserTg.tg_id == msg.from_user.id) 
    .options(selectinload(User.reading_books), selectinload(User.minutes_per_day), selectinload(User.pages_per_day))
)
    dataset = await get_statistics(user, session)
    if dataset:
        html = f"""
	    	<b>Ваша статистика</b>\n
	    <strong>- Всего прочитанно книг:</strong> {dataset['books_count']}\n
	    <strong>- Всего прочитанно страниц:</strong> {dataset['pages_count']}\n
	    <strong>- Слов в минуту:</strong> {dataset['words_per_min']}\n
	    <strong>- Минут в день:</strong> {dataset['minutes_per_day']}\n
	    <strong>- Страниц в месяц:</strong> {dataset['pages_per_month']}\n
	    <strong>- Книг в месяц:</strong> {dataset['books_per_month']}\n
	    	"""
        await msg.answer(f'{html}', parse_mode='HTML')

async def get_pages_per_week(user, session):
    last_minutes =  await session.scalars(select(MinutesPerDay).where(MinutesPerDay.user_id == user.id, MinutesPerDay.date.between(datetime.datetime.now().date()-datetime.timedelta(days=7), datetime.datetime.now().date())))
    last_minutes = last_minutes.all()
    dataset = {"ПН":0,"ВТ":0,"СР":0,"ЧТ":0,"ПТ":0,"СБ":0,"ВС":0 }
    for i in last_minutes:
        dataset[dates[i.date.weekday()]] = i.minutes_count

    fig, ax = plt.subplots()
    d = list(dataset.keys())
    d_values = list(dataset.values())
    ax.barh(d, d_values)  
    ax.set_title('Страниц за неделю')

    # сохранение в буфер, чтобы не сохранять локально
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0) 

    photo = BufferedInputFile(buffer.read(), filename='plot.png')
    plt.close(fig)
    return photo

async def get_books_last_12_months(user, session):
    last_books = await session.scalars(select(Reading_Book).where(Reading_Book.finish_to_read.between(datetime.datetime.now().date()-datetime.timedelta(days=365), datetime.datetime.now().date())))
    last_books = last_books.all()
    dataset = {
        "Январь": 1,
        "Февраль": 1,
        "Март": 1,
        "Апрель": 1,
        "Май": 1,
        "Июнь": 1,
        "Июль": 1,
        "Август": 1,
        "Сентябрь": 1,
        "Октябрь": 1,
        "Ноябрь": 1,    
        "Декабрь": 1
    }
    
    for i in last_books:
        dataset[monthes[i.finish_to_read.month]] += 1
    
    d_values = list(dataset.values())
    
    def func(pct, allvalues):
        absolute = int(pct/100. * sum(allvalues))-1
        return "{:d}".format(absolute)

    fig, ax = plt.subplots(figsize=(8, 8))  
    ax.pie(
        d_values,
        labels=list(dataset.keys()), 
        textprops=dict(color="black"),  
        autopct=lambda pct: func(pct, d_values), 
        labeldistance=1.1
    )
    ax.set_title('Количество прочитанных книг в каждом месяце')
    
    # сохранение в буфер, чтобы не сохранять локально
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0) 

    photo = BufferedInputFile(buffer.read(), filename='plot.png')
    plt.close(fig)
    return photo

    
async def get_minutes_per_week(user, session):
    last_minutes =  await session.scalars(select(MinutesPerDay).where(MinutesPerDay.user_id == user.id, MinutesPerDay.date.between(datetime.datetime.now().date()-datetime.timedelta(days=7), datetime.datetime.now().date())))
    last_minutes = last_minutes.all()
    dataset = {"ПН":0,"ВТ":0,"СР":0,"ЧТ":0,"ПТ":0,"СБ":0,"ВС":0 }
    for i in last_minutes:
        dataset[dates[i.date.weekday()]] = i.minutes_count
        
    fig, ax = plt.subplots()
    d = list(dataset.keys())
    d_values = list(dataset.values())
    ax.barh(d, d_values)  
    ax.set_title('Минут за неделю')

    # сохранение в буфер, чтобы не сохранять локально
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0) 

    photo = BufferedInputFile(buffer.read(), filename='plot.png')
    plt.close(fig)
    return photo

# Удобное полученик конкретной функции графика
GRAPHS = {
    'minutes_per_week': get_minutes_per_week,
    'pages_per_week': get_pages_per_week,
    'books_last_12_months':  get_books_last_12_months
}

@router.message(F.text == markups['analytics'])
async def analytics_handler(msg: types.Message, session: AsyncSession, state: FSMContext):

    await msg.answer(text="Выберите какой график вы хотите получить:", reply_markup=analytics_markup)
    await state.set_state(ChooseGraphState.choose)
    

@router.callback_query(lambda c: c.data in analytics_markups)
async def analytics_graph_handler(callback_query: CallbackQuery, session: AsyncSession):
    selected_option = callback_query.data 
    user = await session.scalar(
    select(User)
        .join(UserTg, User.id == UserTg.user_id)
        .where(UserTg.tg_id == callback_query.from_user.id
) 
    )

    # Логика обработки в зависимости от выбранной кнопки
    if analytics_markups[selected_option]:
        photo = await GRAPHS[selected_option](user, session)
        await callback_query.message.answer_photo(photo=photo)
    

    # Подтверждаем получение callback
    await callback_query.answer()

 
