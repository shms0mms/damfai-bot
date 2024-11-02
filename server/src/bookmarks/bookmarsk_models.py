
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey

from server.src.db import Base
from server.src.books.books_models import Book

class FavouriteUser(Base):
    
    __tablename__ = "favourite_user_table"


    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"),  primary_key=True)
    book:Mapped["Book"] = relationship(uselist=False)


class BookmarkUser(Base):
    
    __tablename__ = "bookmark_user_table"

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    page_id:Mapped[int] = mapped_column(ForeignKey("page_table.id"), primary_key=True)
    

