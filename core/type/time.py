import pendulum
from math import log10, floor

class DateType:
    __slots__ = ["timestamp", "date"]

    def __init__(self, time, /):
        """
        Initialize DateType from timestamp or ISO date string.
        Raises ValueError for unknown formats.
        """
        if self._check_is_timestamp(time):
            self.date = self._parse_timestamp_to_date(time)
        else:
            self.date = pendulum.parse(time)
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
    def _check_is_timestamp(time):
        """
        Check if the value is a valid numeric timestamp.
        """
        try:
            float(time)
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
