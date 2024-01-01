from functools import cached_property
from strawberry.fastapi import BaseContext

from src.user.models import UserModel
from utils.security import decode_jwt_token

from core.exeptions.schema import NoValidTokenRaw


class AuthContext(BaseContext):
    @cached_property
    def current_user(self) -> UserModel:
        try:
            authorization = self.request.headers.get("Authorization", None)
            token = authorization.replace(
                "Bearer ", "") if authorization else None
            dict_user = decode_jwt_token(token=token).get("user")
            return UserModel(**dict_user)
        except:
            raise NoValidTokenRaw


async def get_context() -> AuthContext:
    return AuthContext()
