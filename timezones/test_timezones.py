import datetime
import os.path

import pytest

from . import _defs, tz_rendering, tz_utils, zones

GEOIP_DATA_LOCATION = os.path.abspath(
    os.path.join(__file__, "..", "..", "GeoIP2-City-Test.mmdb")
)


def assert_is_lower(offset_a, offset_b):
    # Force a real sort to happen: to avoid optimizations from kicking in, make
    # sure the list is really out of the expected order, and not in reverse
    # order either.
    coll = ["+9999", offset_b, "-9999", offset_a]
    coll.sort(key=zones._tz_offset_key)
    assert coll[1] == offset_a


def test_sort():
    assert_is_lower("+0100", "+0400")
    assert_is_lower("+0400", "+0430")
    assert_is_lower("+0430", "+0500")

    assert_is_lower("-1000", "+0430")
    assert_is_lower("-1030", "-0500")

    assert_is_lower("-1030", "+0000")

    assert_is_lower("-0030", "+0030")

    assert_is_lower("-0045", "-0030")
    assert_is_lower("+0030", "+0045")


def test_get_timezone():
    assert tz_utils.get_timezone("Europe/Moscow") is not None
    assert tz_utils.get_timezone("Europe/Moscow1") is None
    assert tz_utils.get_timezone("GMT +1:00") is not None

    assert tz_utils.is_valid_timezone("GMT +1:00")
    assert tz_utils.is_valid_timezone("Europe/Moscow")
    assert tz_utils.is_valid_timezone("Europe/Moscow1") is False


@pytest.fixture
def geoip_db():
    try:
        import geoip2  # noqa: F401
    except ImportError:
        pytest.skip("geoip2 not installed")
    if not os.path.exists(GEOIP_DATA_LOCATION):
        pytest.skip("No GeoIP2 database")

    tz_utils.GEOIP_DATA_LOCATION = GEOIP_DATA_LOCATION
    yield
    tz_utils.GEOIP_DATA_LOCATION = None


def test_guess_timezone_geoip(geoip_db):
    assert tz_utils.guess_timezone_by_ip("000.000.000.000", only_name=True) is None
    assert tz_utils.guess_timezone_by_ip("127.0.0.1", only_name=True) is None

    # This uses the MaxMind test DBs; source:
    # https://github.com/maxmind/MaxMind-DB/blob/main/source-data/GeoIP2-City-Test.json
    assert (
        tz_utils.guess_timezone_by_ip("149.101.100.0", only_name=True)
        == "America/Chicago"
    )
    assert tz_utils.guess_timezone_by_ip("2001:230::1", only_name=True) == "Asia/Seoul"

    # Addresses not in the test DB
    assert tz_utils.guess_timezone_by_ip("1.2.3.4", only_name=True) is None
    assert (
        tz_utils.guess_timezone_by_ip("2001:2002:2003:2004::0", only_name=True) is None
    )


def test_guess_timezone_no_geoip():
    assert tz_utils.guess_timezone_by_ip("149.101.100.0", only_name=True) is None
    assert tz_utils.guess_timezone_by_ip("2001:230::1", only_name=True) is None


def test_get_timezones():
    assert len(list(zones.get_timezones(only_us=True))) == 8


@pytest.mark.parametrize("offset_str,tzname,verbose_name", zones.get_timezones())
def test_valid_offset(offset_str, tzname, verbose_name):
    assert tz_utils.is_valid_timezone(tzname)
    tz = tz_utils.get_timezone(tzname)
    assert tz

    # 1. Find a timestamp without DST shift
    now = datetime.datetime.utcnow()
    winter_time = datetime.datetime(now.year, 1, 1)
    summer_time = datetime.datetime(now.year, 7, 1)

    # Looking for a timestamp with zero DST offset
    for ts in [winter_time, summer_time]:
        if tz.dst(ts) == datetime.timedelta(0):
            break
    else:
        assert False, "No timestamp with zero DST offset"

    # 2. Take tz shift without DST
    offset_full_minutes = int(tz.utcoffset(ts).total_seconds() / 60)
    offset_sign = "+" if offset_full_minutes >= 0 else "-"

    offset_hours = abs(offset_full_minutes) // 60
    offset_minutes = abs(offset_full_minutes) - (offset_hours * 60)
    expected_offset = "%s%02d%02d" % (offset_sign, offset_hours, offset_minutes)
    assert offset_str == expected_offset, "Invalid offset for {}".format(tzname)

    # 3. Test verbose name
    assert verbose_name.startswith("(GMT%s) " % expected_offset)


def test_get_timezones_json():
    json_list = tz_rendering.get_timezones_json()
    assert "US/" in json_list


@pytest.mark.parametrize("tzname", _defs._TZ_ALIASES.keys())
def test_aliases(tzname):
    _, name, formatted = tz_utils.format_tz_by_name(tzname)
    assert name == tzname
    assert tzname in formatted
