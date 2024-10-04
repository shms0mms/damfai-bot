from db import Base
from sqlalchemy.orm import mapped_column, Mapped

class Message(Base):
    __tablename__ = 'message'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    username: Mapped[str]
    text: Mapped[str]
    

