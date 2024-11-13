import os.path
import re
import zoneinfo

import pytest

from . import _defs, tz_rendering, tz_utils, zones


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


def test_get_timezones():
    assert len(list(zones.get_timezones(only_us=True))) == 8


@pytest.mark.parametrize("offset_str,tzname,verbose_name", zones.get_timezones())
def test_valid_offset(offset_str, tzname, verbose_name):
    assert tz_utils.is_valid_timezone(tzname)
    tz = tz_utils.get_timezone(tzname)
    assert tz

    # 1. Find a timestamp without DST shift
    dt = tz_utils.get_last_datetime_without_dst(tz)

    # 2. Take tz shift without DST
    offset_full_minutes = int(tz.utcoffset(dt).total_seconds() / 60)
    offset_sign = "+" if offset_full_minutes >= 0 else "-"

    offset_hours = abs(offset_full_minutes) // 60
    offset_minutes = abs(offset_full_minutes) - (offset_hours * 60)
    expected_offset = "%s%02d%02d" % (offset_sign, offset_hours, offset_minutes)
    assert offset_str == expected_offset, f"Invalid offset for {tzname}"

    # 3. Test verbose name
    assert verbose_name.startswith("(GMT%s) " % expected_offset)


def obsolete_names():
    names = {}
    with open("tzdata2023c/backward", "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("Link\t"):
                continue
            _link, dest, source, *_ = re.split("\t+", line)
            names[source] = dest
    return names

@pytest.fixture(name="obsolete_names", scope="session")
def obsolete_names_fixture():
    obsolete_names()

@pytest.mark.parametrize("_offset_str,tzname,_verbose_name", zones.get_timezones())
def test_obsolete_names(_offset_str, tzname, _verbose_name, obsolete_names):
    assert tzname not in obsolete_names.keys(), f"{tzname} is obsolete, use {obsolete_names[tzname]} instead"


def common_names(obsolete_names):
    # TODO: This should be in the library, not a fixture.
    return [
        z for z in zoneinfo.available_timezones()
        if (z not in obsolete_names.keys() and
            "/" in z and
            not z.startswith("SystemV/") and
            not z.startswith("Etc/"))
    ]


@pytest.mark.parametrize("tzname", common_names(obsolete_names()))
def test_missing_names(tzname):
    assert tzname in zones.get_timezones_dict().keys()


def test_get_timezones_json():
    json_list = tz_rendering.get_timezones_json()
    assert "US/" in json_list


@pytest.mark.parametrize("tzname", _defs._TZ_ALIASES.keys())
def test_aliases(tzname):
    _, name, formatted = tz_utils.format_tz_by_name(tzname)
    assert name == tzname
    assert tzname in formatted
