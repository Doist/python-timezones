from datetime import datetime, timedelta

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
    assert verbose_name.startswith(f"(GMT{expected_offset}) ")


def test_get_timezones_json():
    json_list = tz_rendering.get_timezones_json()
    assert "US/" in json_list


@pytest.mark.parametrize("tzname", _defs._TZ_ALIASES.keys())
def test_aliases(tzname):
    _, name, formatted = tz_utils.format_tz_by_name(tzname)
    assert name == tzname
    assert tzname in formatted


def test_get_timezones_lists_vancouver():
    # Given British Columbia has its own timezone from November 2026
    vancouver_labels = []

    # When the supported timezones are listed
    all_timezones = zones.get_timezones()

    # Then America/Vancouver is offered under its own name
    for offset_str, tzname, verbose_name in all_timezones:
        if tzname == "America/Vancouver":
            vancouver_labels.append(verbose_name)
    assert len(vancouver_labels) == 1
    assert vancouver_labels[0].endswith(") Vancouver")


def test_get_timezones_lists_edmonton():
    # Given Alberta has its own timezone from November 2026
    edmonton_labels = []

    # When the supported timezones are listed
    all_timezones = zones.get_timezones()

    # Then America/Edmonton is offered under its own name
    for offset_str, tzname, verbose_name in all_timezones:
        if tzname == "America/Edmonton":
            edmonton_labels.append(verbose_name)
    assert len(edmonton_labels) == 1
    assert edmonton_labels[0].endswith(") Edmonton")


def test_get_timezones_lists_winnipeg():
    # Given Manitoba has its own timezone from November 2026
    winnipeg_labels = []

    # When the supported timezones are listed
    all_timezones = zones.get_timezones()

    # Then America/Winnipeg is offered under its own name
    for offset_str, tzname, verbose_name in all_timezones:
        if tzname == "America/Winnipeg":
            winnipeg_labels.append(verbose_name)
    assert len(winnipeg_labels) == 1
    assert winnipeg_labels[0].endswith(") Winnipeg")


def test_get_timezones_offers_us_central_time_only_for_us_central():
    # Given Manitoba no longer follows US Central time from November 2026
    central_time_zone_names = []

    # When the supported timezones are listed
    all_timezones = zones.get_timezones()

    # Then "Central Time (US & Canada)" is offered only for US/Central
    for offset_str, tzname, verbose_name in all_timezones:
        if verbose_name.endswith(") Central Time (US & Canada)"):
            central_time_zone_names.append(tzname)
    assert central_time_zone_names == ["US/Central"]


def test_get_timezones_keeps_central_america_on_utc_minus_6():
    # Given a date in December 2026, after Manitoba stops changing its clocks
    december_2026 = datetime(2026, 12, 1, 12, 0)
    central_america_zone_names = []

    # When the supported timezones are listed
    all_timezones = zones.get_timezones()

    # Then "Central America" is offered once, on a zone that is at UTC-6 then
    for offset_str, tzname, verbose_name in all_timezones:
        if verbose_name.endswith(") Central America"):
            central_america_zone_names.append(tzname)
    assert len(central_america_zone_names) == 1
    central_america_zone = tz_utils.get_timezone(central_america_zone_names[0])
    assert central_america_zone is not None
    assert central_america_zone.utcoffset(december_2026) == timedelta(hours=-6)
