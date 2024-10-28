import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from ..db import Base

from ..app_auth.auth_models import User

class PagesPerDay(Base):

    __tablename__ = "pages_per_day_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    date:Mapped[datetime.date] = mapped_column()
    pages_count:Mapped[int] = mapped_column(default=0)

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))

    user:Mapped["User"] = relationship(uselist=False, back_populates="pages_per_day")

class MinutesPerDay(Base):

    __tablename__ = "minutes_per_day_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    date:Mapped[datetime.date] = mapped_column()
    minutes_count:Mapped[float] = mapped_column(default=0)

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(uselist=False, back_populates="minutes_per_day")
