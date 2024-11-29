from core.exeptions.helpers import exeption_handling_decorator
from core.type import ResponseAPI, ResponseType
from db.session import get_session
from fastapi import APIRouter, Depends, Header, WebSocket, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from .dals import AuthDAL
from .responses import POST_TOKEN_REFRESH_RESPONSE, POST_TOKEN_RESPONSES
from .schemas import ResponseDOCSType
from .responses import POST_TOKEN_RESPONSES, POST_TOKEN_REFRESH_RESPONSE
from core.type.type import ResponseAPI, ResponseType

auth_router = APIRouter()


@auth_router.post("/token", status_code=status.HTTP_200_OK, responses=POST_TOKEN_RESPONSES)
@exeption_handling_decorator
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends()):
    try:
        async with get_session() as db_session:
            dals = AuthDAL(db_session)
            response = await dals.get_token_user(email=data.username, password=data.password)

            return JSONResponse(content={**ResponseType(loc=[], msg="You have successfully got a session in the Deepmode service!",
                                                        reason="", type="success", input=response.model_dump()).model_dump(), "access_token": response.access_token},
                                status_code=200, headers={"Authorization": response.access_token})

    except:
        raise


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=ResponseType, responses=POST_TOKEN_REFRESH_RESPONSE)
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



@auth_router.websocket("/session_manager")
async def get_start_session(websocket: WebSocket):
    await websocket.accept()
    return {"es": True}