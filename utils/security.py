import utils.user_issues as user_issue_instance
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwt, JWTError


from strawberry.types import Info
from strawberry.permission import BasePermission


from src.user.models import UserModel, PortalRole
from utils.basic import contains_with_list
from core.exeptions.schemas import NoValidTokenRaw


from settings import settings


class JWTAuth(BasePermission):
    message = "You have not been authenticated. You do not have access to this source."

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        authorization = info.context.request.headers.get(
            "Authorization", None)

        token = authorization.replace("Bearer ", "") if authorization else None
        try:
            decode_dict = decode_jwt_token(token=token)
            now = round(datetime.now().timestamp())
            if now >= decode_dict.get("exp"):
                raise

            check_user = await user_issue_instance.check_user_by_email_or_id_in_db(
                user_id=decode_dict.get("user").get("user_id"))

            if check_user is None:
                raise

            return True
        except Exception:
            return False


def create_access_token(user: UserModel, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    encoded_jwt = jwt.encode(
        {"user": user.toJson, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> dict:
    try:
        decoded_dict = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)

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
    ACCESS_ROLES = [PortalRole.ROLE_PORTAL_ADMIN,
                    PortalRole.ROLE_PORTAL_SUPERADMIN]

    return contains_with_list(list_contains=roles,
                              compare_list=ACCESS_ROLES)
