from datetime import datetime


ONE_DAY_IN_SECONDS = 86400


def is_utc_greater_now_utc(utc_data: float, day_spaced: int = 0) -> bool:
    now_date = datetime.utcnow().timestamp()

    try:
        utc_data = utc_data + \
            (day_spaced * ONE_DAY_IN_SECONDS) + (ONE_DAY_IN_SECONDS / 2)

        return True if utc_data <= now_date else False
    except Exception:
        return False
