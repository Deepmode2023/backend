from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request

from .schemas import CreateUserRequest, ResponseUser
from .dals import UserDAL
from db.session import get_session

from utils.user_issues import oauth2_schema

guest_router = APIRouter()
user_router = APIRouter(dependencies=[Depends(oauth2_schema)])


@guest_router.post("/", response_model=ResponseUser)
async def create_user(data: CreateUserRequest):
    async with get_session() as db_session:
        dals = UserDAL(db_session)
        user_account = await dals.create_user_account(
            name=data.name, surname=data.surname, email=data.email, password=data.password)

        return ResponseUser(**user_account.toJson)


@user_router.post("/me", response_model=ResponseUser)
async def get_user_details(request: Request):
    return request.user
