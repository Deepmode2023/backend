from fastapi import status, HTTPException, Depends
from sqlalchemy import select, or_
from enum import Enum
from typing import Union
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer

import utils.security as security_utils
from src.user.models import UserModel
from utils.hasher import hasher_instance
from db.session import get_session
from core.exeptions.schemas import NoValidTokenRaw
from core.schema.schemas import TReturnedModel


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/auth/token", auto_error=False)


class RaiseUpByUserCondition(str, Enum):
    EXIST = "EXIST"
    NOT_EXIST = "NOT_EXIST"


def raise_email_with_detail(detail: str, headers: dict = {"WWW-Authenticate": "Bearer"}):
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         detail=detail, headers=headers)


async def current_user(token: str = Depends(oauth2_schema)) -> Union[UserModel, TReturnedModel]:
    try:
        dict_from_token = security_utils.decode_jwt_token(token=token)
        expire_time = dict_from_token.get("exp")
        now = round(datetime.now().timestamp())
        if now >= expire_time:
            return TReturnedModel(details="The token time has expired!", status=status.HTTP_401_UNAUTHORIZED, data=None)

        user = await check_user_by_email_or_id_in_db(user_id=dict_from_token.get('user').get('user_id'))

        return user

    except Exception:
        return TReturnedModel(details=NoValidTokenRaw().get_message, status=status.HTTP_400_BAD_REQUEST, data=None)


async def check_user_by_email_or_id_in_db(email: Union[str, None] = None, user_id: Union[str, None] = None,  raise_up_by_user_condition: RaiseUpByUserCondition = RaiseUpByUserCondition.EXIST) -> Union[UserModel, None]:
    async with get_session() as db_session:
        user = await db_session.scalars(select(UserModel).filter(
            or_(UserModel.email == email, UserModel.user_id == user_id)
        ))
        user = user.one_or_none()

        if user is None:
            raise NoValidTokenRaw

        if raise_up_by_user_condition == RaiseUpByUserCondition.EXIST:
            if not user:
                raise raise_email_with_detail(
                    "Email or user id is not registred with us.")
        else:
            if user:
                raise raise_email_with_detail(
                    "Email or user id already exist with us.")
    return user


async def check_credential_user(email: str, password: str) -> Union[UserModel, None]:
    user = await check_user_by_email_or_id_in_db(email=email)

    if not hasher_instance.verify_password(plain_password=password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Your token is not valid. You are denied access!", headers={"WWW-Authenticate": "Bearer"})

    return user
