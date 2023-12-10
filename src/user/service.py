from fastapi import APIRouter, Depends, Request, Form, status
from typing import Annotated, Union
from pydantic import EmailStr
from fastapi import File, UploadFile

from core.exeptions.schemas import ThisFileIsNotPicture, YouDontHaveAccessExeptions

from .models import UserModel
from .schemas import ResponseUser
from .dals import UserDAL
from core.schema.schemas import TReturnedModel
from core.exeptions.helpers import responses_status_errors, exeption_handling_decorator
from utils.security import get_current_user, is_admin_checked
from utils.image import ImageCreaterModel
from utils.params_helpers import checked_params_on_none
from db.session import get_session

from utils.user_issues import oauth2_schema

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


@user_router.put("/update_user", response_model=Union[bool, TReturnedModel], responses={**responses_status_errors})
@exeption_handling_decorator
async def update_user(me: UserModel = Depends(get_current_user), name: Annotated[Union[str, None], Form()] = None, surname: Annotated[Union[str, None], Form()] = None, email: Annotated[Union[EmailStr, None], Form()] = None, password: Annotated[Union[str, None], Form()] = None, avatar: UploadFile = File(None)):
    params = checked_params_on_none(
        **{"name": name, "surname": surname, "email": email, "password": password})
    async with get_session() as db_session:
        dals = UserDAL(db_session=db_session)
        try:
            is_access = is_admin_checked(roles=me.roles)
            email = email if email != None else me.email

            if is_access or me.email == email:
                user_account = await dals.update_user_account(image_instance=ImageCreaterModel(image=avatar), **params)
                return True
            else:
                raise YouDontHaveAccessExeptions(
                    reason="for change metadata user!")
        except ThisFileIsNotPicture:
            return TReturnedModel(details=ThisFileIsNotPicture().get_message, status=status.HTTP_400_BAD_REQUEST, data=None)
        except Exception:
            raise
