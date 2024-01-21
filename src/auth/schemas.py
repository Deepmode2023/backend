from pydantic import BaseModel
from enum import Enum


class TypeTokenEnum(str, Enum):
    BEARER = "Bearer"
    COCKIES = "Cockies"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expire_time: int
    type_token:  str = TypeTokenEnum.BEARER.value


## DOCS SECTION ##

class ResponseDOCSDetailsType(BaseModel):
    type: str
    loc: list[str]
    msg: str
    input: TokenResponse
    ctx: str


class ResponseDOCSType(BaseModel):
    details: list[ResponseDOCSDetailsType]


class ResponsePostTokenDOCSType(BaseModel):
    access_token: str
    details: list[ResponseDOCSDetailsType]
