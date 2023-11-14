from pydantic import BaseModel

from .models import ThemeColor


class ReturnedPreference(BaseModel):
    theme: ThemeColor
    shared_mode: bool


class ReturnedSharedPreference(BaseModel):
    details: str
    status_code: int
    data: ReturnedPreference | None
