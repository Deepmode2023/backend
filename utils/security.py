from datetime import datetime, timedelta
from typing import Optional, Any
from fastapi import status, HTTPException, Depends
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from strawberry.types import Info
from strawberry.permission import BasePermission

from modules.user.models import UserModel
from db.session import get_db
from .user_issues import check_user_by_email_or_id_in_db


from settings import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


class JWTAuth(BasePermission):
    message = "You have not been authenticated. You do not have access to this source."

    async def authenticate(self, connect):
        if connect.get("path") in "/api/graphql":
            return None
        else:
            guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()

            if 'authorization' not in connect.headers:
                return guest

            token_raw = connect.headers.get('authorization', None)
            token = get_token_hash(token_raw=token_raw)

            if token == None:
                return guest
            try:
                user = await get_current_user(token=token)
                return AuthCredentials(['authenticated']), user
            except HTTPException:
                return guest

    async def has_permission(self, source: Any, info: Info, **kwargs,) -> bool:
        token_raw = info.context.get_raw_token
        token = get_token_hash(token_raw=token_raw)

        if token == None:
            return False

        try:
            await get_current_user(token=token)
            return True
        except HTTPException:
            return False


def get_token_hash(token_raw: str) -> str:
    TOKEN_HASH_POSITION = 1

    token = token_raw.split(' ')
    token = token[TOKEN_HASH_POSITION] if 0 <= TOKEN_HASH_POSITION < len(
        token) else None

    return token


async def get_current_user(token: str = Depends(oauth2_schema)):
    async with await anext(get_db()) as db_session:
        payload = decode_jwt_token(token=token)

        user_id = payload.get("user", None).get("user_id", None)
        if not user_id:
            return None

        return await check_user_by_email_or_id_in_db(db_session=db_session, user_id=user_id)


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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token errors.")

    return decoded_dict


def create_refresh_token(user_id: str):
    encoded_jwt = jwt.encode(
        {"user_id": user_id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
