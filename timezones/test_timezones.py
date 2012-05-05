import zones
import tz_utils


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


def test_guess_timezone():
    tz_utils.GEOIP_DATA_LOCATION = '/usr/local/geo_ip/GeoLiteCity.dat'
    assert tz_utils.guess_timezone_by_ip('201.246.115.62', only_name=True) == 'Chile/Continental'
    assert tz_utils.guess_timezone_by_ip('000.000.000.000', only_name=True) == None
    assert tz_utils.guess_timezone_by_ip('127.0.0.1', only_name=True) == None


def test_get_timezonez():
    assert len(list(zones.get_timezones(only_us=True))) == 8
