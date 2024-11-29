from .schemas import ResponseCreateDOCSType
from core.type.type import ResponseType
from .exeptions import DontAllowChangeUser
from core.exeptions.schema import DontExistItemInsideDB
from core.exeptions.schema import NoValidTokenRaw

from core.exeptions.schema import YouDontHaveAccessExeptions

from utils.image import ThisFileIsNotPicture


CREATE_USER_RESPONSES = {201: {"model": ResponseCreateDOCSType,
                               "description": "You have successfully created an account."},
                         400: {"model": ResponseType, "description": ThisFileIsNotPicture().get_message},
                         404: {"model": ResponseType, "description": DontExistItemInsideDB().get_message}}


ME_USER_RESPONSES = {
    200: {"model": ResponseCreateDOCSType},
    400: {"model": ResponseType, "description": NoValidTokenRaw().get_message}
}


UPDATE_USER_RESPONSES = {403: {"model": ResponseType, "description": DontAllowChangeUser().get_message},
                         200: {"model": ResponseCreateDOCSType, "description": "Successfull update user ..."},
                         404: {"model": ResponseType, "description": ThisFileIsNotPicture().get_message}}


DELETE_USER_RESPONSES = {200: {"model": ResponseCreateDOCSType, "description": "You successfully deleted the user's email address ..."},
                         401: {"model": ResponseType, "description": YouDontHaveAccessExeptions(reason="for delete metadata user!").get_message},
                         404: {"model": ResponseType, "description": DontExistItemInsideDB().get_message}}
