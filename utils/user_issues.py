from fastapi import status, Depends
from sqlalchemy import select, or_
from enum import Enum
from typing import Union
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer

import utils.security as security_utils
from src.user.models import UserModel
from utils.hasher import hasher_instance
from core.exeptions.schema import (
    NoValidTokenRaw,
    AlreadyExistInDB,
    DontExistItemInsideDB,
    DoNotValidCredential,
)

from db.call import scalars_fetch_one_or_none
from core.type.type import ExceptionResponseAPI


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)


class RaiseUpByUserCondition(str, Enum):
    EXIST = "EXIST"
    NOT_EXIST = "NOT_EXIST"


async def current_user(token: str = Depends(oauth2_schema)) -> UserModel:
    try:
        dict_from_token = security_utils.decode_jwt_token(token=token)

        expire_time = dict_from_token.get("exp")
        now = round(datetime.now().timestamp())
        if now >= expire_time:
            return ExceptionResponseAPI(
                msg="The token time has expired!",
                header={"Authorization": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                input={},
                reason="The token time has expired!",
            )

        user = await check_user_by_email_or_id_in_db(
            user_id=dict_from_token.get("user").get("user_id")
        )

        return user

    except Exception:
        return ExceptionResponseAPI(
            msg=NoValidTokenRaw().get_message,
            header={"Authorization": "Bearer"},
            status_code=status.HTTP_400_BAD_REQUEST,
            input={},
            reason=NoValidTokenRaw().get_message,
        )


async def check_user_by_email_or_id_in_db(
    email: Union[str, None] = None,
    user_id: Union[str, None] = None,
    raise_up_by_user_condition: RaiseUpByUserCondition = RaiseUpByUserCondition.NOT_EXIST,
) -> UserModel:
    user = await scalars_fetch_one_or_none(
        stmp=select(UserModel).filter(
            or_(UserModel.email == email, UserModel.user_id == user_id)
        )
    )

    if raise_up_by_user_condition == RaiseUpByUserCondition.EXIST:
        if user:
            raise AlreadyExistInDB
    else:
        if not user:
            raise DontExistItemInsideDB

    return user


async def check_credential_user(email: str, password: str) -> UserModel:
    user = await check_user_by_email_or_id_in_db(email=email)

    if not hasher_instance.verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        raise DoNotValidCredential

    return user
