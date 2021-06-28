from datetime import (datetime, timezone)


LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo

def get_current_time():
    return datetime.now(tz=LOCAL_TIMEZONE)

def parse_isostring_with_tz(isostring: str):
    return datetime.strptime(isostring, "%Y-%m-%dT%H:%M:%S%z")
