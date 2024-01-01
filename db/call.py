
from sqlalchemy import ScalarResult, CursorResult
from .session import get_session


async def scalars_fetch_one_or_none(stmp, with_commit: bool = False):
    async with get_session() as db_sesion:
        stmp_scalars: ScalarResult = await db_sesion.scalars(stmp)
        if with_commit:
            await db_sesion.commit()
        return stmp_scalars.one_or_none()


async def add_fetch_one_item(smtp):
    async with get_session() as db_sesion:
        cursor: CursorResult = await db_sesion.execute(smtp)
        await db_sesion.commit()
        return cursor.scalar_one_or_none()


async def add_fetch_many_items(models: list):
    async with get_session() as db_sesion:
        result = db_sesion.add_all(models)
        await db_sesion.commit()

        return result.returning()


async def scalars_fetch_many(stmp, with_commit: bool = False):
    async with get_session() as db_sesion:
        stmp_scalars: ScalarResult = await db_sesion.scalars(stmp)
        if with_commit:
            await db_sesion.commit()
        return stmp_scalars.all()
