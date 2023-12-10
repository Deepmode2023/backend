
from sqlalchemy import Update, ScalarResult
from .session import get_session


async def scalars_fetch_one_or_none(stmp, with_commit: bool = False):
    async with get_session() as db_sesion:
        stmp_scalars: ScalarResult = await db_sesion.scalars(stmp)
        if with_commit:
            await db_sesion.commit()
        return stmp_scalars.one_or_none()
