from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
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
        print("END SESSION <====+++++ END SESSION")
        await session.close()


class AsyncSessionContextManager:
    def __init__(self):
        self.close_event = asyncio.Event()

    @contextmanager
    def get_db(self) -> AsyncSession:
        """Context manager for getting async session"""
        print('IM HERE MASSSSS')
        session: AsyncSession = async_session()
        try:
            yield session
        finally:
            self.close_event.wait()  # Wait for the event to be set
            session.close()
            print("Session is closed")

    def unblock_close(self):
        self.close_event.set()  # Unblock the session close


# Инициализируем менеджер контекста
session_manager = AsyncSessionContextManager()
