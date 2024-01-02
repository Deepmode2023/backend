from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, APIRouter, Depends, Header

from .dals import AuthDAL
from db.session import get_session
from core.exeptions.helpers import exeption_handling_decorator


from core.type import ResponseAPI, ResponseType

auth_router = APIRouter()


@auth_router.post("/token", status_code=status.HTTP_200_OK)
@exeption_handling_decorator
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends()):
    try:
        async with get_session() as db_session:
            dals = AuthDAL(db_session)
            response = await dals.get_token_user(email=data.username, password=data.password)
            return response
    except:
        raise


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=ResponseType)
@exeption_handling_decorator
async def authenticate_refresh_token(refresh_token: str = Header()):
    try:
        async with get_session() as db_session:
            dals = AuthDAL(db_session)
            response = await dals.get_refresh_token(refresh_token=refresh_token)
            return ResponseAPI(msg="You have successfully updated the session in the Deepmode service!",
                               reason="", input=response.model_dump(), status_code=status.HTTP_200_OK)
    except:
        raise
