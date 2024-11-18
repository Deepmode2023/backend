from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
import pendulum

ONE_DAY_IN_SECONDS = 86400


def is_utc_greater_now_utc(utc_data: float, day_spaced: int = 0) -> bool:
    now_date = datetime.utcnow().timestamp()

    try:
        utc_data = (
            utc_data + (day_spaced * ONE_DAY_IN_SECONDS) + (ONE_DAY_IN_SECONDS / 2)
        )

        return True if utc_data <= now_date else False
    except Exception:
        return False


class RequestDateType(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = None


@dataclass
class TimeManager:
    timezone = pendulum.now().timezone
    current_date = pendulum.now(tz=pendulum.now().timezone)
    date = pendulum.now(tz=pendulum.now().timezone)

    def __init__(
        cls, date: Optional[RequestDateType] = None, isReturnTimestamp: bool = False
    ):
        cls.isReturnTimestamp = isReturnTimestamp
        if date is not None:
            cls.setNewDate(date=date)

    def format_to_datetime(cls, withUtc: bool = False) -> str:
        return (
            cls.date.format("YYYY-MM-DD HH:mm:ss Z")
            if withUtc
            else cls.date.to_datetime_string()
        )

    def set_new_date(cls, date: RequestDateType):
        cls.date = cls.date.set(**date.model_dump(), tz=cls.timezone)
        return cls.date

    @property
    def get_date(cls):
        return cls.date

