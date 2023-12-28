import datetime


def now() -> datetime.datetime:
    """Create and return a datetime for now."""
    offset = datetime.timedelta(hours=-6)
    return datetime.datetime.now(datetime.timezone(offset))
