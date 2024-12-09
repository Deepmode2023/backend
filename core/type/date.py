from math import floor, log10

import pendulum
from pydantic import BaseModel, ValidationInfo, validator
from pydantic_core import core_schema


class DateType:
    date: pendulum
    timestamp: int

    def __init__(self, date, /):
        """
        Initialize DateType from timestamp or ISO date string.
        Raises ValueError for unknown formats.
        """
        self.date = date
        self.timestamp = self.date.timestamp()

    def __repr__(self):
        return f"DateType(timestamp={self.timestamp}, date={self.date})"

    def __eq__(self, value):
        other_timestamp = self._get_timestamp(value)
        return other_timestamp is not None and self.timestamp == other_timestamp

    def __lt__(self, value):
        other_timestamp = self._get_timestamp(value)
        return other_timestamp is not None and self.timestamp < other_timestamp

    def __gt__(self, value):
        other_timestamp = self._get_timestamp(value)
        return other_timestamp is not None and self.timestamp > other_timestamp

    def _get_timestamp(self, value):
        if isinstance(value, DateType):
            return value.timestamp
        elif isinstance(value, (int, float)):
            return value
        elif hasattr(value, "timestamp") and callable(value.timestamp):
            return value.timestamp()
        return None

    @staticmethod
    def _check_is_timestamp(date):
        """
        Check if the value is a valid numeric timestamp.
        """
        try:
            float(date)
            return True
        except ValueError:
            return False

    @staticmethod
    def _parse_timestamp_to_date(timestamp):
        """
        Parse timestamp of different resolutions into pendulum.DateTime.
        Supports seconds, milliseconds, microseconds, and nanoseconds.
        """
        timestamp = float(timestamp)
        length = floor(log10(timestamp)) + 1

        if length == 10:  # Second Timestamp
            return pendulum.from_timestamp(timestamp)
        elif length == 13:  # Millisecond Timestamp
            return pendulum.from_timestamp(timestamp / 1000)
        elif length == 16:  # Microsecond Timestamp
            return pendulum.from_timestamp(timestamp / 1e6)
        elif length == 19:  # Nanosecond Timestamp
            return pendulum.from_timestamp(timestamp / 1e9)
        else:
            raise ValueError("Unknown timestamp format")

    @classmethod
    def _parse_str_to_date(cls, date: str):
        """
        Check passing date str on pendulum date format
        """
        if isinstance(date, str):
            return pendulum.parse(date)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.with_info_plain_validator_function(
            cls.validate_date_field, metadata={"type": "string"}
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler):
        return {
            "type": "string",
            "description": "A string containing only alphabetic characters.",
        }

    @classmethod
    def validate_date_field(cls, date: str | int, _: ValidationInfo):
        """
        Check field on correct string or integer type
        """
        try:
            if cls._check_is_timestamp(date):
                return cls._parse_timestamp_to_date(date)

            return cls._parse_str_to_date(date)
        except:
            raise ValueError(
                f"Arguments date={date} is encorrect. You must pass integer equal 10-19 chars or str with correct date format = year/month/day"
            )
