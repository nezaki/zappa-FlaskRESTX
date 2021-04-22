from datetime import datetime, timedelta, timezone


def get_jst_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=9)))


def get_utc_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=0)))
