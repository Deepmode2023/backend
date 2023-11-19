from fastapi import status, APIRouter, Depends
from typing import Optional, Union
from db.session import get_session

from utils.security import oauth2_schema
from .dals import SharedPreferenceDAL
from .models import ThemeColor
from core.schema.schemas import TReturnedModel
from .schemas import ReturnedSharedPreference

from core.exeptions.schemas import UnknownExceptions

from core.exeptions.helpers import exeption_handling_decorator


preference_router = APIRouter()


@preference_router.get("/", summary="Get Shared Preference", status_code=status.HTTP_200_OK, response_model=Union[ReturnedSharedPreference, TReturnedModel])
@exeption_handling_decorator
async def get_shared_preference(token_raw: str = Depends(oauth2_schema)):
    try:
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.get_shared_preference(
                token_raw=token_raw)

            return ReturnedSharedPreference(details="Returned shared preference.", status=status.HTTP_200_OK, data=[shared_preference_instance.to_json])
    except Exception:
        raise UnknownExceptions


@preference_router.put("/", summary="Change Shared Preference", status_code=status.HTTP_200_OK, response_model=Union[ReturnedSharedPreference, TReturnedModel])
@exeption_handling_decorator
async def put_shared_preference(token_raw: str = Depends(oauth2_schema), theme: Optional[ThemeColor] = None, shared_mode: Optional[bool] = None):
    try:
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.put_shared_preference(token_raw=token_raw, theme=theme, shared_mode=shared_mode)

            return ReturnedSharedPreference(details="Returned shared preference.", status=status.HTTP_200_OK, data=[shared_preference_instance.to_json])
    except Exception:
        raise UnknownExceptions
