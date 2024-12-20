from datetime import datetime

from fastapi import APIRouter, Depends, Form, status
from typing import Annotated, Union
from pydantic import EmailStr
from fastapi import File, UploadFile

from core.exeptions.schema import YouDontHaveAccessExeptions

from .models import UserModel
from .exeptions import DontAllowChangeUser
from .schemas import ResponseUser
from .dals import UserDAL
from .responses import CREATE_USER_RESPONSES, ME_USER_RESPONSES, UPDATE_USER_RESPONSES, DELETE_USER_RESPONSES


from utils.security import is_admin_checked
from utils.user_issues import current_user
from utils.basic import build_kwargs_not_none
from utils.image import ImageCreaterModel, ThisFileIsNotPicture
from utils.time import is_utc_greater_now_utc
from utils.dict import extract_key_or_value
from utils.user_issues import oauth2_schema

from db.session import get_session
from core.type.type import ExceptionResponseAPI, ResponseType, ResponseAPI
from core.exeptions.helpers import exeption_handling_decorator
from core.exeptions.schema import DontExistItemInsideDB

guest_router = APIRouter()
user_router = APIRouter(dependencies=[Depends(oauth2_schema)])


@guest_router.post("/", status_code=201, response_model=ResponseType, responses=CREATE_USER_RESPONSES)
@exeption_handling_decorator
async def create_user(name: Annotated[str, Form()], surname: Annotated[str, Form()], email: Annotated[EmailStr, Form()], password: Annotated[str, Form()], avatar: UploadFile = File(None)):
    try:

        async with get_session() as db_session:
            dals = UserDAL(db_session=db_session)
            user_account = await dals.create_user_account(image_instance=ImageCreaterModel(image=avatar),
                                                          name=name, surname=surname, email=email, password=password)
            response_data = ResponseUser(user_id=str(user_account.user_id),
                                         **extract_key_or_value(user_account.toJson, ["user_id"]))

        return ResponseAPI(msg="You have successfully created an account.", status_code=status.HTTP_201_CREATED,
                           input=response_data.model_dump())
    except ThisFileIsNotPicture:
        return ExceptionResponseAPI(msg=ThisFileIsNotPicture().get_message, status_code=status.HTTP_400_BAD_REQUEST, input={})

    except Exception:
        raise


@user_router.post("/me", status_code=200, response_model=ResponseType,  responses=ME_USER_RESPONSES)
async def get_user_details(current_user: UserModel = Depends(current_user)):
    return ResponseAPI(msg="Your account details.", input=current_user.toJson, reason="")


@user_router.put("/update_user", status_code=200, response_model=ResponseType, responses=UPDATE_USER_RESPONSES)
@exeption_handling_decorator
async def update_user(email: Annotated[EmailStr, Form()], current_user: UserModel = Depends(current_user), name: Annotated[Union[str, None], Form()] = None, surname: Annotated[Union[str, None], Form()] = None, avatar: UploadFile = File(None)):
    params = build_kwargs_not_none(
        **{"name": name, "surname": surname})
    try:
        async with get_session() as db_session:
            dals = UserDAL(db_session=db_session)

            is_access = is_admin_checked(roles=current_user.roles)
            last_update = current_user.updated_account.timetuple()
            if is_access or is_utc_greater_now_utc(utc_data=datetime(last_update.tm_year,
                                                                     last_update.tm_mon, last_update.tm_mday,
                                                                     last_update.tm_hour).timestamp(), day_spaced=-1):
                if is_access or current_user.email == email:
                    user_account = await dals.update_user_account(email=email, image_instance=ImageCreaterModel(image=avatar), **params)
                    return ResponseAPI(msg=f"Successfull update user {user_account.email}", status_code=status.HTTP_200_OK,
                                       input=ResponseUser(**user_account.toJson).model_dump())
                else:
                    raise YouDontHaveAccessExeptions(
                        reason="for change metadata user!")
            else:
                return ExceptionResponseAPI(msg=DontAllowChangeUser().get_message, input={}, reason=DontAllowChangeUser().get_message,
                                            status_code=status.HTTP_403_FORBIDDEN,)
    except ThisFileIsNotPicture:
        return ExceptionResponseAPI(msg=ThisFileIsNotPicture().get_message, status=status.HTTP_400_BAD_REQUEST,
                                    input={}, reason=ThisFileIsNotPicture().get_message)
    except Exception:
        raise


@user_router.delete("/delete_user", status_code=200,  response_model=ResponseType, responses=DELETE_USER_RESPONSES)
@exeption_handling_decorator
async def delete_user(email: Annotated[EmailStr, Form()], current_user: UserModel = Depends(current_user)):
    try:
        if isinstance(current_user, UserModel):
            is_access = is_admin_checked(roles=current_user.roles)
            if is_access or email == current_user.email:
                async with get_session() as db_session:
                    dals = UserDAL(db_session=db_session)
                    delete_user = await dals.delete_user(email=email)

                    return ResponseAPI(msg=f"You successfully deleted the user's email address {delete_user.email}", status_code=status.HTTP_200_OK,
                                       input=ResponseUser(**delete_user.toJson).model_dump(), reason="")
            else:
                raise YouDontHaveAccessExeptions(
                    reason="for delete metadata user!")
        else:
            raise DontExistItemInsideDB
    except Exception:
        raise
