import asyncio
from asyncpg.exceptions import CannotConnectNowError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase


from config import config

engine  = create_async_engine(url = config.env.DATABASE_URL )

session = sessionmaker(engine,class_=AsyncSession )


async def get_session():
    async with session() as connection:
        yield connection

        
class Base(DeclarativeBase):
    ...
async def create_db():
    await asyncio.sleep(5) 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def main():
    try:
        await create_db()
    except CannotConnectNowError as exc:
        print(f"Failed to connect to database: {exc}")

