from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models import SharedPreferenceModel

from utils.basic import build_kwargs_not_none
from core.exeptions.schema import DoNotUpdateFieldsInDB
from src.user.models import UserModel

from db.call import scalars_fetch_one_or_none


class SharedPreferenceDAL:
    def __init__(self, db_session):
        self.db_session: AsyncSession = db_session

    async def get_shared_preference(self, current_user: UserModel):
        stmp = select(SharedPreferenceModel).where(
            SharedPreferenceModel.user_id == current_user.user_id)

        return await scalars_fetch_one_or_none(stmp=stmp)

    async def put_shared_preference(self, current_user: UserModel, **kwargs) -> SharedPreferenceModel | None:
        not_none_kwargs = build_kwargs_not_none(
            except_kwargs=["token_raw", "is_admin", "user"], **kwargs)

        if len(not_none_kwargs) > 0:
            stmp = update(SharedPreferenceModel).where(SharedPreferenceModel.user_id ==
                                                       current_user.user_id).values(**not_none_kwargs).returning(SharedPreferenceModel)
            return await scalars_fetch_one_or_none(stmp=stmp)
        else:
            raise DoNotUpdateFieldsInDB
