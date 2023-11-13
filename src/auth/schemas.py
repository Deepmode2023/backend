from pydantic import BaseModel
from enum import Enum


class TypeTokenEnum(str, Enum):
    BEARER = "Bearer"
    COCKIES = "Cockies"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expire_time: int
    type_token: TypeTokenEnum = TypeTokenEnum.BEARER
