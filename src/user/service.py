from datetime import datetime

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Form, status
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
from core.exeptions.schemas import DontExistItemInsideDB

from utils.security import is_admin_checked
from utils.user_issues import current_user
from utils.basic import build_kwargs_not_none
from utils.image import ImageCreaterModel, ThisFileIsNotPicture
from utils.time import is_utc_greater_now_utc
from db.session import get_session

from utils.user_issues import oauth2_schema

guest_router = APIRouter()
user_router = APIRouter(dependencies=[Depends(oauth2_schema)])


@guest_router.post("/", response_model=Union[ResponseTRetunedModel, TReturnedModel])
@exeption_handling_decorator
async def create_user(name: Annotated[str, Form()], surname: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], avatar: UploadFile = File(None)):
    try:
        print(">>>>> sldflsdfl")
        async with get_session() as db_session:
            dals = UserDAL(db_session=db_session)
            user_account = await dals.create_user_account(image_instance=ImageCreaterModel(image=avatar),
                                                          name=name, surname=surname, email=email, password=password)
        return ResponseTRetunedModel(details="You have successfully created an account.",
                                     status=status.HTTP_201_CREATED, data=ResponseUser(**user_account.toJson, updated_account=user_account.updated_account))
    except ThisFileIsNotPicture:
        return TReturnedModel(details=ThisFileIsNotPicture().get_message, status=status.HTTP_400_BAD_REQUEST, data=None)
    except Exception as ex:
        print(">>> exeptions", ex)
        raise


@user_router.post("/me", response_model=Union[ResponseUser, TReturnedModel])
async def get_user_details(current_user: Union[UserModel, TReturnedModel] = Depends(current_user)):
    return current_user


@user_router.put("/update_user", response_model=Union[ResponseTRetunedModel, TReturnedModel], responses={**responses_status_errors, 403: {"model": TReturnedModel, "description": DontAllowChangeUser().get_message}})
@exeption_handling_decorator
async def update_user(email: Annotated[EmailStr, Form()], current_user: Union[UserModel, TReturnedModel] = Depends(current_user), name: Annotated[Union[str, None], Form()] = None, surname: Annotated[Union[str, None], Form()] = None, avatar: UploadFile = File(None)):
    params = build_kwargs_not_none(
        **{"name": name, "surname": surname})
    try:
        if isinstance(current_user, UserModel):
            async with get_session() as db_session:
                dals = UserDAL(db_session=db_session)

                is_access = is_admin_checked(roles=current_user.roles)
                last_update = current_user.updated_account.timetuple()
                if is_access or is_utc_greater_now_utc(utc_data=datetime(last_update.tm_year,
                                                                         last_update.tm_mon, last_update.tm_mday,
                                                                         last_update.tm_hour).timestamp(), day_spaced=1):
                    if is_access or current_user.email == email:
                        user_account = await dals.update_user_account(email=email, image_instance=ImageCreaterModel(image=avatar), **params)
                        return ResponseTRetunedModel(details=f"Successfull update user {user_account.email}",
                                                     status=status.HTTP_200_OK, data=ResponseUser(**user_account.toJson, updated_account=user_account.updated_account))
                    else:
                        raise YouDontHaveAccessExeptions(
                            reason="for change metadata user!")
                else:
                    return TReturnedModel(details=DontAllowChangeUser().get_message, status=status.HTTP_403_FORBIDDEN, data=None)
        else:
            raise DontExistItemInsideDB
    except ThisFileIsNotPicture:
        return TReturnedModel(details=ThisFileIsNotPicture().get_message, status=status.HTTP_400_BAD_REQUEST, data=None)
    except Exception:
        raise


@user_router.delete("/delete_user", response_model=Union[ResponseTRetunedModel, TReturnedModel])
@exeption_handling_decorator
async def delete_user(email: EmailStr, current_user: Union[UserModel, TReturnedModel] = Depends(current_user)):
    try:
        if isinstance(current_user, UserModel):
            is_access = is_admin_checked(roles=current_user.roles)
            if is_access or email == current_user.email:
                async with get_session() as db_session:
                    dals = UserDAL(db_session=db_session)
                    delete_user = await dals.delete_user(email=email)

                    return ResponseTRetunedModel(details=f"You successfully deleted the user's email address {delete_user.email}.",
                                                 status=status.HTTP_200_OK, data=ResponseUser(**delete_user.toJson,
                                                                                              updated_account=delete_user.updated_account))
            else:
                raise YouDontHaveAccessExeptions(
                    reason="for delete metadata user!")
        else:
            raise DontExistItemInsideDB
    except Exception:
        raise
