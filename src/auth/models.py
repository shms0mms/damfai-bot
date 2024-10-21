import datetime
from enum import Enum
import json
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
import typing
from sqlalchemy import text


class UserTg(Base):
    __tablename__ = "user_tg_table"
    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    tg_id:Mapped[int]
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey('user_table.id', ondelete='CASCADE'))
    user:Mapped["User"] = relationship(uselist=False, back_populates="user_tg")


created_at = typing.Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('Europe/Moscow', now())"))]
class Role(Enum):
    user = "user"
    admin = "admin"

class User(Base):
    
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)    
    user_tg:Mapped[list["UserTg"]] = relationship(uselist=True, back_populates="user")
	

    role:Mapped[Role] = mapped_column(default=Role.user)

    password:Mapped[bytes]
    email:Mapped[str] = mapped_column(unique=True)

    name:Mapped[str]
    surname:Mapped[str]
        
    dob:Mapped[datetime.date]
    
    created_at:Mapped[created_at]

    words_per_minute:Mapped[str] = mapped_column(default=json.dumps([120]))



    
  