from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, APIRouter, Depends, Header

from .dals import AuthDAL
from db.session import get_db
from .schemas import TokenResponse

auth_router = APIRouter()


@auth_router.post("/token", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_db)):
    dals = AuthDAL(db_session)
    return await dals.get_token_user(email=data.username, password=data.password)


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def authenticate_refresh_token(refresh_token: str = Header(), db_session: AsyncSession = Depends(get_db)):
    dals = AuthDAL(db_session)
    return await dals.get_refresh_token(refresh_token=refresh_token)
