"""
tz_utils
~~~~~~~~

Includes timezone related utilities.


Example usage (get a fixed offset timezone)::

    print tz_utils.get_timezone('GMT +10:00')


Example usage (guess timezone by IP, required geoip2!)::

    tz_utils.GEOIP_DATA_LOCATION = '/usr/local/geo_ip/GeoIP2-City.mmdb'
    assert tz_utils.guess_timezone_by_ip('201.246.115.62') == 'Chile/Continental'


Example usage (format timezone by name)::

    print tz_utils.format_tz_by_name('Europe/Copenhagen')
        =>
    ("+0100", "Europe/Copenhagen", '(GMT+0100) Copenhagen')


Example usage (is a timezone valid?)::

    print tz_utils.is_valid_timezone('Europe/Copenhagen')
        =>
    True


:copyright: 2012 by Amir Salihefendic ( http://amix.dk/ )
:license: MIT
"""
from __future__ import annotations

import zoneinfo as zi
from datetime import datetime, timedelta, tzinfo

from . import _defs

try:
    import geoip2.database as geoip2_db

    HAS_GEOIP2 = True
except ImportError:
    HAS_GEOIP2 = False

# --- Exports ----------------------------------------------
__all__ = [
    "get_timezone",
    "is_valid_timezone",
    "GEOIP_DATA_LOCATION",
    "guess_timezone_by_ip",
    "format_tz_by_name",
]

# --- Specifies the location of GeoIP GeoLiteCity.dat database ---
GEOIP_DATA_LOCATION = None


# --- Functions ----------------------------------------------
def guess_timezone_by_ip(ip: str, only_name: bool = False):
    """Given an `ip` with guess timezone using geoip2.
    Returns a tuple of (tz_offets, tz_name, tz_formatted).
    `None` is returned if it can't guess a timezone.

    For this to work you need to set tz_utils.GEOIP_DATA_LOCATION
    You can get this database from http://www.maxmind.com/app/geolitecity

    Example usage::

        from timezones import tz_utils
        tz_utils.GEOIP_DATA_LOCATION = '/usr/local/geo_ip/GeoLiteCity.dat'
        assert tz_utils.guess_timezone_by_ip('201.246.115.62') == 'Chile/Continental'

    """
    geo_lib = _get_geoip_lib()
    if geo_lib:
        try:
            record = geo_lib.city(ip)
            if record:
                location = record.location
                if location and location.time_zone:
                    if only_name:
                        return location.time_zone
                    else:
                        return format_tz_by_name(location.time_zone)
        except Exception:
            record = None
    return None


def get_timezone(tzname: str) -> tzinfo | None:
    """Get a timezone instance by name or return `None`.

    This getter support fixed offest timezone like `get_timezone('GMT +10:00')`"""
    try:
        # First, try with the provided name
        return zi.ZoneInfo(tzname)
    except zi.ZoneInfoNotFoundError:
        pass

    # No result: try with an alias, if there's one
    if alias := (_defs._TZ_ALIASES.get(tzname)):
        try:
            return zi.ZoneInfo(alias)
        except zi.ZoneInfoNotFoundError:
            pass

    # Still no result: fallback to a static timezone, or return None
    return _tz_map().get(tzname)


def is_valid_timezone(timezone: str) -> bool:
    """Return `True` if the `timezone` is valid. Otherwise `False` is returned."""
    try:
        tz = get_timezone(timezone)
        if tz:
            return True
        else:
            return False
    except Exception:
        return False


def format_tz_by_name(tz_name: str, tz_formatted: str | None = None) -> _defs.Timezone:
    """Returns a tuple of (tz_offets, tz_name, tz_formatted).

    >>> format_tz_by_name("Europe/Copenhagen")
    ("+0100", "Europe/Copenhagen", "(GMT+0100) Copenhagen")
    >>> format_tz_by_name("America/Sao_Paulo", "Brasilia, Sao Paulo")
    ("-0300", "America/Sao_Paulo", "(GMT-0300) Brasilia, Sao Paulo")
    """
    tz = get_timezone(tz_name)
    if not tz:
        raise ValueError(f"Invalid timezone {tz_name}")

    # Make sure we have a date without DST
    now = datetime.now(tz)
    while (dst := now.dst()) is not None and dst.total_seconds() != 0:
        now += timedelta(days=30)
    offset = now.strftime("%z")

    tz_formatted = f"(GMT{offset}) {tz_formatted or tz_name}"
    return (offset, tz_name, tz_formatted)


# --- Private ----------------------------------------------
GEO_IP = None


def _get_geoip_lib():
    global GEO_IP

    if not HAS_GEOIP2 or not GEOIP_DATA_LOCATION:
        return None

    try:
        GEO_IP = geoip2_db.Reader(GEOIP_DATA_LOCATION)
    except Exception:
        return None

    return GEO_IP


_zero = timedelta(0)


class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.offset = offset
        self.name = name

        self._offset = timedelta(minutes=offset)
        self.zone = name

    def __str__(self):
        return self.zone

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self.zone

    def dst(self, dt):
        return _zero

    def localize(self, dt, is_dst=False):
        """Convert naive time to local time"""
        if dt.tzinfo is not None:
            raise ValueError("Not naive datetime (tzinfo is already set)")
        return dt.replace(tzinfo=self)

    def __getinitargs__(self):
        return (self.offset, self.name)


TZ_MAP = None


def _tz_map():
    global TZ_MAP

    if TZ_MAP is None:
        timezones = [
            FixedOffset(-720, "GMT -12:00"),
            FixedOffset(-660, "GMT -11:00"),
            FixedOffset(-600, "GMT -10:00"),
            FixedOffset(-540, "GMT -9:00"),
            FixedOffset(-480, "GMT -8:00"),
            FixedOffset(-420, "GMT -7:00"),
            FixedOffset(-360, "GMT -6:00"),
            FixedOffset(-300, "GMT -5:00"),
            FixedOffset(-240, "GMT -4:00"),
            FixedOffset(-180, "GMT -3:00"),
            FixedOffset(-120, "GMT -2:00"),
            FixedOffset(-60, "GMT -1:00"),
            FixedOffset(0, "GMT"),
            FixedOffset(60, "GMT +1:00"),
            FixedOffset(120, "GMT +2:00"),
            FixedOffset(180, "GMT +3:00"),
            FixedOffset(240, "GMT +4:00"),
            FixedOffset(300, "GMT +5:00"),
            FixedOffset(360, "GMT +6:00"),
            FixedOffset(420, "GMT +7:00"),
            FixedOffset(480, "GMT +8:00"),
            FixedOffset(540, "GMT +9:00"),
            FixedOffset(600, "GMT +10:00"),
            FixedOffset(660, "GMT +11:00"),
            FixedOffset(720, "GMT +12:00"),
            FixedOffset(780, "GMT +13:00"),
        ]

        TZ_MAP = dict([(z.zone, z) for z in timezones])

    return TZ_MAP
