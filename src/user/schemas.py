from pydantic import BaseModel, EmailStr
from pydantic.dataclasses import dataclass
from fastapi import Form
from typing import Optional, Annotated
from datetime import datetime


@dataclass
class UpdateUserRequest(BaseModel):
    name: Annotated[str, Form()] = None
    surname: Annotated[str, Form()] = None
    password: Annotated[str, Form()] = None
    email: Annotated[EmailStr, Form()] = None
    avatar: Annotated[bytes, Form()] = None


class CreateUserRequest(BaseModel):
    name: str
    surname: str
    password: str
    email: EmailStr


class ResponseUser(BaseModel):
    user_id: str
    name: str
    surname: str
    email: EmailStr
    roles: list[str]
    updated_account: Optional[datetime] = None


## DOCS SECTIONS ##


class ResponseDOCSDetailsType(BaseModel):
    type: str
    loc: list[str]
    msg: str
    input: ResponseUser
    ctx: str


class ResponseCreateDOCSType(BaseModel):
    details: list[ResponseDOCSDetailsType]
