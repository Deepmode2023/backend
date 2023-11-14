from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from utils.security import access_decorator
from .models import SharedPreferenceModel

from utils.basic import build_kwargs_not_none
from core.exeptions.ExeptionsSchema import DoNotUpdateFieldsInDB


class SharedPreferenceDAL:
    def __init__(self, db_session):
        self.db_session: AsyncSession = db_session

    @access_decorator
    async def get_shared_preference(self, token_raw: str, *args, **kwargs):
        instance = await self.db_session.scalars(select(SharedPreferenceModel).where(SharedPreferenceModel.user_id == kwargs.get('user').user_id))
        return instance.one_or_none()

    @access_decorator
    async def put_shared_preference(self, token_raw: str, *args, **kwargs) -> SharedPreferenceModel | None:
        not_none_kwargs = build_kwargs_not_none(
            except_kwargs=["token_raw", "is_admin", "user"], **kwargs)

        if len(not_none_kwargs) > 0:
            instance = await self.db_session.scalar(update(SharedPreferenceModel).where(SharedPreferenceModel.user_id == kwargs.get('user').user_id).values(**not_none_kwargs).returning(SharedPreferenceModel))
            await self.db_session.commit()

            return instance
        else:
            raise DoNotUpdateFieldsInDB
