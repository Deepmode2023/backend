from typing import Any, Optional

import pendulum
from jose import JWTError, jwt
from strawberry.permission import BasePermission
from strawberry.types import Info

import utils.user_issues as user_issue_instance
from core.exeptions.schema import NoValidTokenRaw
from settings import settings
from src.user.models import PortalRole, UserModel
from utils.basic import contains_with_list
from utils.time import RequestDateType


class JWTAuth(BasePermission):
    message = "You have not been authenticated. You do not have access to this source."

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        authorization = info.context.request.headers.get("Authorization", None)

        token = authorization.replace("Bearer ", "") if authorization else None

        try:
            decode_dict = decode_jwt_token(token=token)

            now = pendulum.now().format("x")
            if now >= decode_dict.get("exp"):
                raise

            check_user = await user_issue_instance.check_user_by_email_or_id_in_db(
                user_id=decode_dict.get("user").get("user_id")
            )

            if check_user is None:
                raise

            return True
        except Exception:
            return False


def create_access_token(
    user: UserModel, expires_delta: Optional[RequestDateType] = None
):
    current = pendulum.now(tz=pendulum.now().timezone)
    date = current.add(
        minutes=expires_delta if expires_delta else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    encoded_jwt = jwt.encode(
        {
            "user": user.toJson,
            "exp": date.format("x"),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> dict:
    try:
        decoded_dict = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise NoValidTokenRaw

    return decoded_dict


def create_refresh_token(user_id: str):
    encoded_jwt = jwt.encode(
        {"user_id": user_id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def access_decorator(low_function):
    async def wrapper(*args, **kwargs):
        user_metadata: UserModel = kwargs.get("user")
        is_admin = is_admin_checked(roles=user_metadata.roles)
        return await low_function(is_admin=is_admin, *args, **kwargs)

    return wrapper


def is_admin_checked(roles: list[str]) -> bool:
    ACCESS_ROLES = [PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN]

    return contains_with_list(list_contains=roles, compare_list=ACCESS_ROLES)
