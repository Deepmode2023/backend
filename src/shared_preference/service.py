from fastapi import status, APIRouter, Depends
from typing import Optional, Union
from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from utils.user_issues import oauth2_schema, current_user
from .dals import SharedPreferenceDAL
from .models import ThemeColor
from core.schema.schemas import TReturnedModel
from .schemas import ReturnedSharedPreference

from src.user.models import UserModel
from core.exeptions.schemas import UnknownExceptions
from core.exeptions.helpers import exeption_handling_decorator

preference_router = APIRouter()


@preference_router.get("/", summary="Get Shared Preference",  status_code=status.HTTP_200_OK, response_model=Union[ReturnedSharedPreference, TReturnedModel])
@exeption_handling_decorator
async def get_shared_preference(user: Union[TReturnedModel, UserModel] = Depends(current_user)):
    try:
        if isinstance(user, TReturnedModel):
            return user
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.get_shared_preference(
                user=user)

            return ReturnedSharedPreference(details="Returned shared preference.", status=status.HTTP_200_OK, data=[shared_preference_instance.to_json])
    except Exception as ex:
        raise UnknownExceptions


@preference_router.put("/", summary="Change Shared Preference", status_code=status.HTTP_200_OK, response_model=Union[ReturnedSharedPreference, TReturnedModel])
@exeption_handling_decorator
async def put_shared_preference(user: Union[TReturnedModel, UserModel] = Depends(current_user), theme: Optional[ThemeColor] = None, shared_mode: Optional[bool] = None):
    try:
        if isinstance(user, TReturnedModel):
            return user
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.put_shared_preference(user=user, theme=theme, shared_mode=shared_mode)

            return ReturnedSharedPreference(details="Returned shared preference.", status=status.HTTP_200_OK, data=[shared_preference_instance.to_json])
    except Exception:
        raise UnknownExceptions
