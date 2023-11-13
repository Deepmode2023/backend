from contextlib import asynccontextmanager
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio

from settings import settings


engine = create_async_engine(
    settings.DATABASE_URL_async,
    future=True,
    echo=True,
)

# create session for the interaction with database
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        print("START SESSION <====+++++ START SESSION")
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
        print("END SESSION <====+++++ END SESSION")


@asynccontextmanager
async def get_session():
    session_instance = None
    try:
        async with async_session() as s:
            session_instance = s
            yield session_instance
    except:
        if session_instance:
            await session_instance.rollback()
        raise
    finally:
        if session_instance:
            await session_instance.close()
