from fastapi import status, APIRouter, Depends, Form
from typing import Optional, Annotated
from db.session import get_session

from utils.user_issues import current_user
from .dals import SharedPreferenceDAL
from .models import ThemeColor

from src.user.models import UserModel
from core.exeptions.helpers import exeption_handling_decorator
from .schema import ReturnedPreference


from core.type import ResponseAPI, ResponseType

preference_router = APIRouter()


@preference_router.get("", summary="Get Shared Preference",  status_code=status.HTTP_200_OK, response_model=ResponseType)
@exeption_handling_decorator
async def get_shared_preference(current_user: UserModel = Depends(current_user)):
    try:
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.get_shared_preference(
                current_user=current_user)

            return ResponseAPI(msg="You have successfully obtained Deepmode settings!",
                               status_code=status.HTTP_200_OK, input=ReturnedPreference(**shared_preference_instance.toJson).model_dump())
    except Exception:
        raise


@preference_router.put("", summary="Change Shared Preference", status_code=status.HTTP_200_OK, response_model=ResponseType)
@exeption_handling_decorator
async def put_shared_preference(theme: Annotated[Optional[ThemeColor], Form()] = None, current_user: UserModel = Depends(current_user), shared_mode: Annotated[Optional[bool], Form()] = None):
    try:
        async with get_session() as db_session:
            dals = SharedPreferenceDAL(db_session=db_session)
            shared_preference_instance = await dals.put_shared_preference(current_user=current_user, theme=theme, shared_mode=shared_mode)

            return ResponseAPI(msg="You have successfully changed the Deepmode settings!",
                               status_code=status.HTTP_200_OK, input=ReturnedPreference(**shared_preference_instance.toJson).model_dump())
    except Exception:
        raise
