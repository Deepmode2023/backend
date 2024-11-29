from .schemas import ResponseGetDOCSType

from core.exeptions.schema import DoNotUpdateFieldsInDB
from core.exeptions.schema import NoValidTokenRaw
from core.type.type import ResponseType

GET_SHARED_PREFERNCE_RESPONSES = {
    200: {"description": "You have successfully obtained Deepmode settings!", "model": ResponseGetDOCSType},
    400: {"model": ResponseType, "description": NoValidTokenRaw().get_message}}


UPDATE_SHARED_PREFERENCE_RESPONSES = {
    200: {"description": "You have successfully changed the Deepmode settings!", "model": ResponseGetDOCSType},
    400: {"model": ResponseType, "description": NoValidTokenRaw().get_message},
    404: {"model": ResponseType, "description": DoNotUpdateFieldsInDB().get_message}}
