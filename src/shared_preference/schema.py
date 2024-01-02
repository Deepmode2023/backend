from pydantic import BaseModel
from .models import ThemeColor


class ReturnedPreference(BaseModel):
    theme: ThemeColor
    shared_mode: bool
