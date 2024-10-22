from ..app_auth.auth_models import User
from sqlalchemy.ext.asyncio import AsyncSession
from ..analytics.analytics_models import PagesPerDay, MinutesPerDay
from ..books_to_reading.booksRead_models import Reading_Book
from calendar import monthrange
import datetime
from sqlalchemy import func, select

async def get_statistics(user: User, session: AsyncSession):
    if user:
        user_id = user.id
        
        books_count = await session.scalar(select(func.count(Reading_Book.book_id)).where(Reading_Book.is_read == True))
        pages_count = 0
        for i in user.pages_per_day:
            pages_count += i.pages_count
        minutes_per_day = await session.scalar(select(func.avg(MinutesPerDay.minutes_count)).where(MinutesPerDay.user_id == user_id))
        year = datetime.datetime.now().date().year
        month = datetime.datetime.now().date().month
        start = datetime.date(year, month, 1)
        end = datetime.date(year, month, monthrange(year, month)[1])
        pages_per_month = await session.scalar(select(func.sum(PagesPerDay.pages_count)).where(PagesPerDay.date.between(start, end)))
        books_per_month = await session.scalar(select(func.sum(Reading_Book.book_id)).where(Reading_Book.finish_to_read.between(start, end), Reading_Book.is_read == True))
        words_per_minute:list[int] = eval(user.words_per_minute)
        words_per_min = (sorted(words_per_minute))[round(len(words_per_minute)/2 - 0.5)]
        dataset = {
            "books_count": books_count  or 0,
            "pages_count":pages_count  or 0 ,
            "words_per_min":words_per_min  or 0,
            "minutes_per_day": minutes_per_day  or 0,
            "pages_per_month": pages_per_month or 0,
            "books_per_month": books_per_month  or 0,
        }
        return dict(dataset)