import os
import pytest
import pytz
import datetime
from timezones import zones, tz_utils, tz_rendering

GEOIP_DATA_LOCATION = '/usr/local/geo_ip/GeoIP2-City.mmdb'


def test_sort():
    # +04:00 is bigger than +04:30
    assert zones._sort_by_tzoffset('+0400', '+0430') == -1

    # +04:00 equal to +04:00
    assert zones._sort_by_tzoffset('+0400', '+0400') == 0

    # +05:00 is bigger to +04:30
    assert zones._sort_by_tzoffset('+0500', '+0430') == 1

    # +01:00 is smaller than +04:00
    assert zones._sort_by_tzoffset('+0100', '+0400') == -1

    # -10:00 is smaller than +04:30
    assert zones._sort_by_tzoffset('-1000', '+0430') == -1

    # -05:00 is bigger than -10:00
    assert zones._sort_by_tzoffset('-0500', '-1030') == 1

    # 00:00 is bigger than -10:00
    assert zones._sort_by_tzoffset('+0000', '-1030') == 1


def test_get_timezone():
    assert tz_utils.get_timezone('Europe/Moscow') is not None
    assert tz_utils.get_timezone('Europe/Moscow1') is None
    assert tz_utils.get_timezone('GMT +1:00') is not None

    assert tz_utils.is_valid_timezone('GMT +1:00')
    assert tz_utils.is_valid_timezone('Europe/Moscow')
    assert tz_utils.is_valid_timezone('Europe/Moscow1') is False


def no_geolib():
    return not os.path.exists(GEOIP_DATA_LOCATION)


@pytest.mark.skipif(no_geolib() is True, reason='Requires GeoIP2 database')
def test_guess_timezone():
    tz_utils.GEOIP_DATA_LOCATION = GEOIP_DATA_LOCATION
    assert not tz_utils.guess_timezone_by_ip('70.132.4.78')
    assert tz_utils.guess_timezone_by_ip(
        '201.246.115.62', only_name=True) == 'America/Santiago'
    assert tz_utils.guess_timezone_by_ip(
        '000.000.000.000', only_name=True) is None
    assert tz_utils.guess_timezone_by_ip('127.0.0.1', only_name=True) is None

    tz_utils.GEOIP_DATA_LOCATION = '/usr/local/geo_ip/NotFound.mmdb'
    assert tz_utils.guess_timezone_by_ip(
        '201.246.115.62', only_name=True) is None


def test_get_timezonez():
    assert len(list(zones.get_timezones(only_us=True))) == 8


@pytest.mark.parametrize('offset_str,tzname,verbose_name',
                         zones._ALL_TIMEZONES)
def test_valid_offset(offset_str, tzname, verbose_name):
    tz = pytz.timezone(tzname)

    # 1. Find a timestamp without DST shift
    now = datetime.datetime.utcnow()
    winter_time = datetime.datetime(now.year + 1, 1, 1)
    summer_time = datetime.datetime(now.year + 1, 7, 1)

    # Looking for a timestamp with zero DST offset
    for ts in [winter_time, summer_time]:
        if tz.dst(ts) == datetime.timedelta(0):
            break

    # 2. Take tz shift without DST
    offset_full_minutes = int(tz.utcoffset(ts).total_seconds() / 60)
    offset_sign = '+' if offset_full_minutes >= 0 else '-'

    offset_hours = abs(offset_full_minutes) // 60
    offset_minutes = abs(offset_full_minutes) - (offset_hours * 60)
    expected_offset = '%s%02d%02d' % (offset_sign, offset_hours,
                                      offset_minutes)
    assert offset_str == expected_offset, 'Invalid offset for {}'.format(
        tzname)

    # 3. Test verbose name
    assert verbose_name.startswith("(GMT%s) " % expected_offset)


def test_get_timezones_json():
    json_list = tz_rendering.get_timezones_json()
    assert 'US/' in json_list
