from enum import Enum
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class Role(Enum):
    teacher = "teacher"
    student = "student"
    admin = "admin"
    manager = "manager"


class UserTg(Base):
    __tablename__ = "user_tg_table"
    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    tg_id:Mapped[int]
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey('user_table.id', ondelete='CASCADE'))
    user:Mapped["User"] = relationship(uselist=False, back_populates="user_tg")
class User(Base):
    
    __tablename__ = "user_table"
    
    id:Mapped[uuid.UUID]  = mapped_column(primary_key=True)
    user_tg:Mapped[list["UserTg"]] = relationship(uselist=True, back_populates="user")
	
    name:Mapped[str]    
    surname:Mapped[str]
    patronymic:Mapped[str]
    
    
    password:Mapped[bytes]
    
    email:Mapped[str] = mapped_column(unique=True)
    
    number:Mapped[str] 
        
    role:Mapped[Role]