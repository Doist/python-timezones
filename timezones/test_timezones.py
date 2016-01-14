import pytest
import pytz
import datetime
from timezones import zones, tz_utils, tz_rendering


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
    assert tz_utils.get_timezone('Europe/Moscow') != None
    assert tz_utils.get_timezone('Europe/Moscow1') == None
    assert tz_utils.get_timezone('GMT +1:00') != None

    assert tz_utils.is_valid_timezone('GMT +1:00') == True
    assert tz_utils.is_valid_timezone('Europe/Moscow') == True
    assert tz_utils.is_valid_timezone('Europe/Moscow1') == False


@pytest.mark.xfail
def test_guess_timezone():
    tz_utils.GEOIP_DATA_LOCATION = '/usr/local/geo_ip/GeoIP2-City.mmdb'
    assert tz_utils.guess_timezone_by_ip('201.246.115.62', only_name=True) == 'America/Santiago'
    assert tz_utils.guess_timezone_by_ip('000.000.000.000', only_name=True) == None
    assert tz_utils.guess_timezone_by_ip('127.0.0.1', only_name=True) == None

    tz_utils.GEOIP_DATA_LOCATION = '/usr/local/geo_ip/NotFound.mmdb'
    assert tz_utils.guess_timezone_by_ip('201.246.115.62', only_name=True) == None


def test_guess_timezone_by_javascript():
    asia_yekaterinburg = tz_utils.get_timezone('Asia/Yekaterinburg')
    for i in xrange(2):  # to ensure that cache breaks nothing
        assert tz_utils.guess_timezone_by_javascript('Tue Feb 01 2005 00:00:00 GMT+0500 (YEKT)') == asia_yekaterinburg
        assert tz_utils.guess_timezone_by_javascript('Mon Aug 01 2005 00:00:00 GMT+0600 (YEKST)') == asia_yekaterinburg
        assert tz_utils.guess_timezone_by_javascript('Mon Aug 01 2005 00:00:00 GMT+0600 (OOOPS)') == None

    assert tz_utils.guess_timezone_by_javascript('Tue Feb 01 2005 00:00:00 GMT+0500 (YEKT)', True) == 'Asia/Yekaterinburg'
    assert tz_utils.guess_timezone_by_javascript('Mon Aug 01 2005 00:00:00 GMT+0600 (YEKST)', True) == 'Asia/Yekaterinburg'
    assert tz_utils.guess_timezone_by_javascript('Mon Aug 01 2005 00:00:00 GMT+0600 (OOOPS)', True) == None


def test_get_timezonez():
    assert len(list(zones.get_timezones(only_us=True))) == 8

@pytest.mark.parametrize('offset_str,tzname,verbose_name', zones._ALL_TIMEZONES)
def test_valid_offset(offset_str, tzname, verbose_name):
    tz = pytz.timezone(tzname)

    # 1. Find a timestamp without DST shift
    now = datetime.datetime.utcnow()
    winter_time = datetime.datetime(now.year + 1, 1, 1)
    summer_time = datetime.datetime(now.year + 1, 7, 1)
    for ts in [winter_time, summer_time]:
        if tz.dst(ts) == datetime.timedelta(0):
            break

    # 2. Take tz shift without DST
    offset_full_minutes = int(tz.utcoffset(ts).total_seconds() / 60)
    offset_sign = '+' if offset_full_minutes >= 0 else '-'

    offset_hours = abs(offset_full_minutes) / 60
    offset_minutes = abs(offset_full_minutes) - (offset_hours * 60)
    expected_offset = '%s%02d%02d' % (offset_sign, offset_hours, offset_minutes)
    assert offset_str == expected_offset

    # 3. Test verbose name
    assert verbose_name.startswith("(GMT%s) " % expected_offset)

def test_get_timezones_json():
    json_list = tz_rendering.get_timezones_json()
    assert 'US/' in json_list
