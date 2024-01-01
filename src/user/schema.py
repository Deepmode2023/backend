from pydantic import BaseModel, EmailStr
from pydantic.dataclasses import dataclass
from fastapi import Form
from typing import Union, Optional, Annotated, Dict
from core.schema.schemas import TReturnedModel
from uuid import UUID
from datetime import datetime
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
    user_id: str
    name: str
    surname: str
    email: EmailStr
    roles: list[str]
    updated_account: Optional[datetime] = None


class ResponseTRetunedModel(TReturnedModel):
    data: ResponseUser


class MessageResponse(BaseModel):
    status_code: int
    detail: str
    header: Optional[str] = None


class ErrorResonseUser(BaseModel):
    message: Union[MessageResponse, ResponseUser]


class CheckedEmailCondition(str, Enum):
    EXIST: "EXIST"
    NOT_EXIST: "NOT_EXIST"
