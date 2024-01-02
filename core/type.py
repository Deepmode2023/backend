from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from typing import Optional


from utils.params_helpers import check_on_wierd_type_and_return_str


class ResponseCtx(BaseModel):
    reason: str


class ResponseDetailType(BaseModel):
    type: str
    loc: list[str]
    msg: str
    input: dict
    ctx: ResponseCtx


class ResponseType(BaseModel):
    def __init__(cls, type: str, loc: list[str], msg: str, input: dict, reason: str):
        super().__init__(detail=[ResponseDetailType(
            type=type, loc=loc, msg=msg, input=input, ctx=ResponseCtx(reason=reason))])

    detail: list[ResponseDetailType]


## ------------------------------- TOTAL TYPE FOR API --------------------------------- ##

def ResponseAPI(msg: str, input: dict, reason: str = "", loc: list[str] = [],
                header: Optional[dict] = None, status_code: int = 200) -> JSONResponse:
    content = ResponseType(type="success", loc=loc,
                           msg=msg, input={key: check_on_wierd_type_and_return_str(input[key]) for key in input}, reason=reason).model_dump()
    return JSONResponse(content=content, status_code=status_code, headers=header)


def ExceptionResponseAPI(msg: str, input: dict, status_code: int, reason: str, loc: list[str] = [],
                         header: Optional[dict] = None) -> HTTPException:
    content = ResponseType(type="error", loc=loc,
                           msg=msg, input={key: check_on_wierd_type_and_return_str(input[key]) for key in input}, reason=reason).model_dump()
    raise HTTPException(
        detail=content, status_code=status_code, headers=header)
