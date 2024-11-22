import datetime


__all__ = [
    'ISO8601_FORMAT',
    'get_utc_now',
    'to_iso8601_format',
    'iso8601_duration_format',
    'iso8601_duration_format',
]


ISO8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

_SECONDS_IN_DAY = 24 * 60 * 60
_SECONDS_IN_HOUR = 60 * 60


def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.UTC)


def to_iso8601_format(dt: datetime.datetime) -> str:
    return dt.strftime(ISO8601_FORMAT)


def iso8601_duration_format(td: datetime.timedelta) -> str:
    """Convert timedelta object to ISO 8601 duration string."""
    if td == datetime.timedelta():
        return 'PT0S'

    result = ['P']
    total_seconds = int(td.total_seconds())
    microseconds = td.microseconds

    days, remainder = divmod(total_seconds, _SECONDS_IN_DAY)
    hours, remainder = divmod(remainder, _SECONDS_IN_HOUR)
    minutes, seconds = divmod(remainder, 60)

    weeks, days = divmod(days, 7)
    if weeks:
        result.append(f'{weeks}W')
    if days:
        result.append(f'{days}D')
    if hours or minutes or seconds or microseconds:
        result.append('T')
    if hours:
        result.append(f'{hours}H')
    if minutes:
        result.append(f'{minutes}M')
    if seconds or microseconds:
        result.append(f'{seconds}')
        if microseconds:
            result.append(f'.{microseconds:06d}'.rstrip('0'))
        result.append('S')

    return ''.join(result)


def replace_utc_timezone_with_z(dt_str: str) -> str:
    """ISO 8601 replacement"""
    return dt_str.replace('+00:00', 'Z', 1)
