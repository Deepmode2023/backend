from pydantic import BaseModel
from .models import ThemeColor


class ReturnedPreference(BaseModel):
    theme: ThemeColor
    shared_mode: bool


class ResponseDOCSDetailsType(BaseModel):
    type: str
    loc: list[str]
    msg: str
    input: ReturnedPreference
    ctx: str


class ResponseGetDOCSType(BaseModel):
    details: list[ResponseDOCSDetailsType]
