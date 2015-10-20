# -*- coding: utf-8 -*-
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

import pytz
import re

try:
    import geoip2.database as geoip2_db
except:
    geoip2_db = None

from datetime import tzinfo, timedelta, datetime


#--- Exports ----------------------------------------------
__all__ = ['get_timezone', 'is_valid_timezone',
           'GEOIP_DATA_LOCATION', 'guess_timezone_by_ip',
           'format_tz_by_name']


#--- Specifies the location of GeoIP GeoLiteCity.dat database ---
GEOIP_DATA_LOCATION = None


#--- Functions ----------------------------------------------
def guess_timezone_by_ip(ip, only_name=False):
    """Given an `ip` with guess timezone using geoip2.
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
                if location:
                    timezone = location.time_zone
                    if only_name:
                        return timezone
                    else:
                        return format_tz_by_name(timezone)
        except:
            record = None
    return None


# the map tzname -> timezone string (YEKT -> "Asia/Yekaterinburg",
#                                    YEKST -> "Asia/Yekaterinburg" and so on)
_tzname_cache = {}

def guess_timezone_by_javascript(date_string, only_name=False):
    """Given the `date_string` as returned by JavaScript, tries to return the
    user browser timezone.

    Example usage::

        from timezones import tz_utils
        assert tz_utils.guess_timezone_by_javascript('Tue Feb 01 2005 00:00:00 GMT+0500 (YEKT)', only_name=True) == 'Asia/Yekaterinburg'

    You may get the javascript date representation as::

        new Date().toString()

    Implementation note: currently we ignore the tz offset component of the
    date string object, and rely on the timezone name in parentheses only.
    """

    def obj_or_name(obj):
        """ helper function returning timezone object or its name only"""
        if obj and only_name:
            return obj.zone
        return obj

    if not date_string:
        return None

    chunks = date_string.split()
    datetime_info = ' '.join(chunks[:5])  # "Tue Feb 01 2005 00:00:00"
    timezone_info = chunks[5:]  # ['GMT+0500', '(YEKT)']

    if len(timezone_info) != 2:
        return None

    try:
        dt = datetime.strptime(datetime_info, '%a %b %d %Y %H:%M:%S')
    except ValueError:  # unable to convert string to datetime object
        return None

    expected_tzname = timezone_info[1].strip('()')

    if expected_tzname in _tzname_cache:
        # check in cache first (cache stores srings or None`s)
        timezone_name = _tzname_cache[expected_tzname]
        if not timezone_name:
            return None
        timezone_obj = pytz.timezone(timezone_name)
        return obj_or_name(timezone_obj)

    for timezone in pytz.all_timezones:
        timezone_obj = pytz.timezone(timezone)
        tzname = timezone_obj.tzname(dt)
        _tzname_cache[tzname] = timezone
        if tzname == expected_tzname:
            break
    else:
        _tzname_cache[expected_tzname] = None
        return None

    return obj_or_name(timezone_obj)



def get_timezone(tzname):
    """Get a timezone instance by name or return `None`.

    This getter support fixed offest timezone like `get_timezone('GMT +10:00')`"""
    try:
        tz = pytz.timezone(tzname)
    except (KeyError, IOError):
        tz = _tz_map().get(tzname)
    return tz


def is_valid_timezone(timezone):
    """Return `True` if the `timezone` is valid. Otherwise `False` is returned."""
    try:
        tz = get_timezone(timezone)
        if tz:
            return True
        else:
            return False
    except:
        return False


def format_tz_by_name(tz_name, tz_formated=None):
    """Returns a tuple of (tz_offets, tz_name, tz_formated).

    Example::
        format_tz_by_name('Europe/Copenhagen')
            =>
        ("+0100", "Europe/Copenhagen", '(GMT+0100) Copenhagen')
    """
    now = datetime.now(get_timezone(tz_name))
    offset = now.strftime("%z")

    if tz_formated:
        tz_formated = re.sub('\(GMT.+?\)', '(GMT%s)' % offset, tz_formated)
    else:
        tz_formated = '(GMT%s) %s' % (offset, tz_name)

    return (offset, tz_name, tz_formated)



#--- Private ----------------------------------------------
GEO_IP = None
def _get_geoip_lib():
    global GEO_IP

    if not GEOIP_DATA_LOCATION:
        return None

    try:
        GEO_IP = geoip2_db.Reader(GEOIP_DATA_LOCATION)
    except:
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
        '''Convert naive time to local time'''
        if dt.tzinfo is not None:
            raise ValueError, 'Not naive datetime (tzinfo is already set)'
        return dt.replace(tzinfo=self)

    def __getinitargs__(self):
        return (self.offset, self.name)


TZ_MAP = None
def _tz_map():
    global TZ_MAP

    if TZ_MAP is None:
        timezones = [
            FixedOffset(-720, 'GMT -12:00'), FixedOffset(-660, 'GMT -11:00'),
            FixedOffset(-600, 'GMT -10:00'), FixedOffset(-540, 'GMT -9:00'),
            FixedOffset(-480, 'GMT -8:00'),  FixedOffset(-420, 'GMT -7:00'),
            FixedOffset(-360, 'GMT -6:00'),  FixedOffset(-300, 'GMT -5:00'),
            FixedOffset(-240, 'GMT -4:00'),  FixedOffset(-180, 'GMT -3:00'),
            FixedOffset(-120, 'GMT -2:00'),  FixedOffset(-60, 'GMT -1:00'),
            FixedOffset(0, 'GMT'),           FixedOffset(60, 'GMT +1:00'),
            FixedOffset(120, 'GMT +2:00'),   FixedOffset(180, 'GMT +3:00'),
            FixedOffset(240, 'GMT +4:00'),   FixedOffset(300, 'GMT +5:00'),
            FixedOffset(360, 'GMT +6:00'),   FixedOffset(420, 'GMT +7:00'),
            FixedOffset(480, 'GMT +8:00'),   FixedOffset(540, 'GMT +9:00'),
            FixedOffset(600, 'GMT +10:00'),  FixedOffset(660, 'GMT +11:00'),
            FixedOffset(720, 'GMT +12:00'),  FixedOffset(780, 'GMT +13:00')]

        TZ_MAP = dict([(z.zone, z) for z in timezones])

    return TZ_MAP
