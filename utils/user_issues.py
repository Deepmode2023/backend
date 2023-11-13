from fastapi import status, HTTPException
from sqlalchemy import select, or_
from enum import Enum
from typing import Union

from src.user.models import UserModel
from utils.hasher import hasher_instance
from db.session import get_session


class RaiseUpByUserCondition(str, Enum):
    EXIST = "EXIST"
    NOT_EXIST = "NOT_EXIST"


def raise_email_with_detail(detail: str, headers: dict = {"WWW-Authenticate": "Bearer"}):
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         detail=detail, headers=headers)


async def check_user_by_email_or_id_in_db(email: Union[str, None] = None, user_id: Union[str, None] = None,  raise_up_by_user_condition: RaiseUpByUserCondition = RaiseUpByUserCondition.EXIST) -> Union[UserModel, None]:
    async with get_session() as db_session:
        user = await db_session.scalars(select(UserModel).filter(
            or_(UserModel.email == email, UserModel.user_id == user_id)
        ))
        user = user.one_or_none()

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
                            detail="Invalid credential.", headers={"WWW-Authenticate": "Bearer"})

    return user
