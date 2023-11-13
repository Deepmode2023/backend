from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from .schemas import TokenResponse
from utils.security import create_access_token, create_refresh_token, decode_jwt_token
from utils.user_issues import check_credential_user, check_user_by_email_or_id_in_db
from settings import settings


class AuthDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_refresh_token(self, refresh_token: str) -> TokenResponse:
        token_decode = decode_jwt_token(token=refresh_token)
        user = await check_user_by_email_or_id_in_db(
            user_id=token_decode.get('user_id', None))

        expire_second = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).seconds
        access_token = create_access_token(user=user)

        return TokenResponse(access_token=access_token, refresh_token=refresh_token, expire_time=expire_second)

    async def get_token_user(self, email: str, password: str) -> TokenResponse:
        user = await check_credential_user(email=email, password=password)
        expire_second = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).seconds
        access_token = create_access_token(user=user)
        refresh_token = create_refresh_token(user_id=str(user.user_id))

        return TokenResponse(access_token=access_token, refresh_token=refresh_token, expire_time=expire_second)
