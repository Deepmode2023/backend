from pydantic import BaseModel
from typing import Union

from .models import ThemeColor, SharedPreferenceModel
from core.schema.schemas import TReturnedModel


class ReturnedPreference(BaseModel):
    theme: ThemeColor
    shared_mode: bool


class ReturnedSharedPreference(TReturnedModel):
    data: Union[list[ReturnedPreference], None]
