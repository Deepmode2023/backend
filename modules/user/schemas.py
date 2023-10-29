from pydantic import BaseModel, EmailStr
from typing import Union
from uuid import UUID
from enum import Enum


class CreateUserRequest(BaseModel):
    name: str
    surname: str
    password: str
    email: EmailStr


class ResponseUser(BaseModel):
    user_id: UUID
    name: str
    surname: str
    email: EmailStr
    roles: list[str]


class MessageResponse(BaseModel):
    status_code: int
    detail: str
    header: Union[str, None]


class ErrorResonseUser(BaseModel):
    message: Union[MessageResponse, ResponseUser]


class CheckedEmailCondition(str, Enum):
    EXIST: "EXIST"
    NOT_EXIST: "NOT_EXIST"
