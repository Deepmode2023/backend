from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_async_engine(
    settings.DATABASE_URL_async,
    future=True,
    echo=True,
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_session() -> AsyncGenerator:
    session_instance = None
    try:
        async with async_session() as session:
            session_instance = session
            yield session_instance
    except:
        if session_instance:
            await session_instance.rollback()
        raise
    finally:
        if session_instance:
            await session_instance.close()
