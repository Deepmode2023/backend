from fastapi import status, APIRouter, Depends, HTTPException
from typing import Optional
from db.session import get_session

from utils.security import oauth2_schema
from .dals import SharedPreferenceDAL
from .models import ThemeColor
from .schemas import ReturnedSharedPreference
from core.exeptions.ExeptionsSchema import DoNotUpdateFieldsInDB

preference_router = APIRouter()


@preference_router.get("/", summary="Get Shared Preference", status_code=status.HTTP_200_OK, response_model=ReturnedSharedPreference)
async def get_shared_preference(token_raw: str = Depends(oauth2_schema)):
    try:
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.get_shared_preference(
                token_raw=token_raw)

            return ReturnedSharedPreference(details="Returned shared preference.", status_code=status.HTTP_200_OK, data=shared_preference_instance.to_json)

    except Exception as ex:
        print("exeptions ====> ", ex)
        return ReturnedSharedPreference(details="Something went wrong and you'll be contacted in the future.", status_code=status.HTTP_409_CONFLICT, data=None)


@preference_router.put("/", summary="Change Shared Preference", status_code=status.HTTP_200_OK, response_model=ReturnedSharedPreference)
async def get_shared_preference(token_raw: str = Depends(oauth2_schema), theme: Optional[ThemeColor] = None, shared_mode: Optional[bool] = None):
    try:
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.put_shared_preference(token_raw=token_raw, theme=theme, shared_mode=shared_mode)

            return ReturnedSharedPreference(details="Returned shared preference.", status_code=status.HTTP_200_OK, data=shared_preference_instance.to_json)
    except DoNotUpdateFieldsInDB:
        return ReturnedSharedPreference(details=DoNotUpdateFieldsInDB().get_message, status_code=status.HTTP_409_CONFLICT, data=None)

    except Exception as ex:
        print("exeptions ====> ", ex)
        return ReturnedSharedPreference(details="Something went wrong and you'll be contacted in the future.", status_code=status.HTTP_409_CONFLICT, data=None)
