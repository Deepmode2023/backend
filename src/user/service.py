from datetime import datetime

from fastapi import APIRouter, Depends, Request, Form, status
from typing import Annotated, Union
from pydantic import EmailStr
from fastapi import File, UploadFile

from core.exeptions.schemas import YouDontHaveAccessExeptions

from .models import UserModel
from .exeptions import DontAllowChangeUser
from .schemas import ResponseUser, ResponseTRetunedModel
from .dals import UserDAL
from core.schema.schemas import TReturnedModel
from core.exeptions.helpers import responses_status_errors, exeption_handling_decorator

from utils.security import get_current_user, is_admin_checked
from utils.basic import build_kwargs_not_none
from utils.image import ImageCreaterModel, ThisFileIsNotPicture
from utils.time import is_utc_greater_now_utc
from db.session import get_session

from utils.security import oauth2_schema

guest_router = APIRouter()
user_router = APIRouter(dependencies=[Depends(oauth2_schema)])


@guest_router.post("/", response_model=ResponseUser)
async def create_user(name: Annotated[str, Form()], surname: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], avatar: Annotated[bytes, File()] = None):
    async with get_session() as db_session:
        dals = UserDAL(db_session=db_session)
        user_account = await dals.create_user_account(
            name=name, surname=surname, email=email, password=password, avatar=avatar)

        return ResponseUser(**user_account.toJson)


@user_router.post("/me", response_model=ResponseUser)
async def get_user_details(request: Request):
    return request.user


@user_router.put("/update_user", response_model=Union[ResponseTRetunedModel, TReturnedModel], responses={**responses_status_errors, 403: {"model": TReturnedModel, "description": DontAllowChangeUser().get_message}})
@exeption_handling_decorator
async def update_user(me: UserModel = Depends(get_current_user), name: Annotated[Union[str, None], Form()] = None, surname: Annotated[Union[str, None], Form()] = None, email: Annotated[Union[EmailStr, None], Form()] = None, password: Annotated[Union[str, None], Form()] = None, avatar: UploadFile = File(None)):
    params = build_kwargs_not_none(
        **{"name": name, "surname": surname, "email": email, "password": password})
    async with get_session() as db_session:
        dals = UserDAL(db_session=db_session)
        try:
            is_access = is_admin_checked(roles=me.roles)
            last_update = me.updated_account.timetuple()
            email = email if email != None else me.email
            if is_access or is_utc_greater_now_utc(utc_data=datetime(last_update.tm_year,
                                                                     last_update.tm_mon, last_update.tm_mday,
                                                                     last_update.tm_hour).timestamp(), day_spaced=1):
                if is_access or me.email == email:
                    user_account = await dals.update_user_account(is_access=is_access, me=me, image_instance=ImageCreaterModel(image=avatar), **params)
                    return ResponseTRetunedModel(details=f"Successfull update user {user_account.email}",
                                                 status=status.HTTP_200_OK, data=ResponseUser(**user_account.toJson, updated_account=user_account.updated_account))
                else:
                    raise YouDontHaveAccessExeptions(
                        reason="for change metadata user!")
            else:
                return TReturnedModel(details=DontAllowChangeUser().get_message, status=status.HTTP_403_FORBIDDEN, data=None)
        except ThisFileIsNotPicture:
            return TReturnedModel(details=ThisFileIsNotPicture().get_message, status=status.HTTP_400_BAD_REQUEST, data=None)
        except Exception:
            raise
