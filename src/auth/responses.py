from .schemas import ResponseDOCSType, ResponsePostTokenDOCSType
from core.type.type import ResponseType
from core.exeptions.schema import DontExistItemInsideDB, DoNotValidCredential


POST_TOKEN_RESPONSES = {200: {"description": "You have successfully got a session in the Deepmode service!", "model": ResponsePostTokenDOCSType},
                        401: {"description": DoNotValidCredential().get_message, "model": ResponseType},
                        404: {"description": DontExistItemInsideDB().get_message, "model": ResponseType}}


POST_TOKEN_REFRESH_RESPONSE = {200: {"description": "You have successfully updated the session in the Deepmode service!", "model": ResponseDOCSType},
                               401: {"description": DoNotValidCredential().get_message, "model": ResponseType},
                               404: {"description": DontExistItemInsideDB().get_message, "model": ResponseType}}
