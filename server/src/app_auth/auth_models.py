import json
import datetime
import uuid
import typing

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from enum import Enum

from server.src.books.books_models import EmoteEnum
if typing.TYPE_CHECKING:   
    from server.src.analytics.analytics_models import PagesPerDay, MinutesPerDay
    from server.src.books.books_models import Book, PageModel
    from server.src.themes.themes_models import Theme
    from server.src.extensions.extensions_models import Extension
 
from server.src.db import Base

class Role(Enum):
    user = "user"
    admin = "admin"
    manager = "manager"
    
    

created_at = typing.Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('Europe/Moscow', now())"))]



class User(Base):
    
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)    
    user_tg:Mapped[list["UserTg"]] = relationship(uselist=True, back_populates="user")

    # служебная инфа
    role:Mapped[Role] = mapped_column(default=Role.user)
    password:Mapped[bytes]
    created_at:Mapped[created_at]
    
    # running
    running_points:Mapped[int] = mapped_column(default=0)

    # user инфа
    email:Mapped[str] = mapped_column(unique=True)
    name:Mapped[str]
    surname:Mapped[str]
    dob:Mapped[datetime.date]
    balance: Mapped[int] = mapped_column(default=0)
    
    
    # analytics data 
    words_per_minute:Mapped[str] = mapped_column(default=json.dumps([120]))


    # bookmarks router
    favourite_books:Mapped[list["Book"]] = relationship(
        back_populates="favourite_for_users",
        uselist=True,
        secondary="favourite_user_table")
    
    bookmarks_on_page:Mapped[list["PageModel"]] = relationship(
        back_populates="bookmarks_for_user",
        uselist=True,
        secondary="bookmark_user_table")
    
    # bookmarks_on_sum_page:Mapped[list["ReadingPage"]] = relationship(
    #     uselist=True,
    #     secondary="sum_bookmark_user_table")
    
    #  theme router
    themes: Mapped[list["Theme"]] = relationship(
        back_populates="users",
        uselist=True,
        secondary="theme_user_table"
    )
    
    #  extension router
    extensions: Mapped[list["Extension"]] = relationship(
        back_populates="users",
        uselist=True,
        secondary="extension_user_table"
    )
    
    #  reading_books router
    reading_books:Mapped[list["Book"]] = relationship(uselist=True, secondary="reading_book_table")

    #  analytics router
    pages_per_day:Mapped[list["PagesPerDay"]] = relationship(back_populates="user", uselist=True)
    minutes_per_day:Mapped[list["MinutesPerDay"]] = relationship(back_populates="user", uselist=True)

    emote: Mapped[EmoteEnum] = mapped_column(default=None, nullable=True)

    
class UserTg(Base):
    __tablename__ = "user_tg_table"
    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    tg_id:Mapped[int]
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey('user_table.id', ondelete='CASCADE'))
    user:Mapped["User"] = relationship(uselist=False, back_populates="user_tg")