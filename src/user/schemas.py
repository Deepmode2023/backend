from pydantic import BaseModel, EmailStr
from pydantic.dataclasses import dataclass
from fastapi import Form
from typing import Union, Optional, Annotated
from uuid import UUID
from enum import Enum


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
    user_id: UUID
    name: str
    surname: str
    email: EmailStr
    roles: list[str]


class MessageResponse(BaseModel):
    status_code: int
    detail: str
    header: Optional[str] = None


class ErrorResonseUser(BaseModel):
    message: Union[MessageResponse, ResponseUser]


class CheckedEmailCondition(str, Enum):
    EXIST: "EXIST"
    NOT_EXIST: "NOT_EXIST"
