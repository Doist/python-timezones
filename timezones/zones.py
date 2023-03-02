"""
zones
~~~~~~~~

Holds a collection of common timezones.
Is much smaller and better formated than pytz.common_timezones.
It also supports fixed timezones such as `GMT +7:00`.

Example usage (returns US based timezones)::

    for tz_offset, tz_name, tz_formated in zones.get_timezones(only_us=True):
        print(tz_formated)

        =>

        "(GMT-1000) Hawaii')"
        "(GMT-0900) Alaska')"
        "(GMT-0800) Pacific Time (US & Canada)"
        ...

:copyright: 2012 by Amir Salihefendic ( http://amix.dk/ )
:license: MIT
"""
from __future__ import annotations

import re

from . import _defs, tz_utils

_RE_TZ_OFFSET = re.compile(r"([+-])(\d\d)(\d\d)")

_updated_all_tzs: list[_defs.Timezone] = []
_updated_us_tzs: list[_defs.Timezone] = []


def get_timezones(
    only_us: bool = False, only_fixed: bool = False
) -> list[_defs.Timezone]:
    """Returns an iterator of timezones.

    `only_us` (optional, defaults to `False`):
        Only return US related timezones

    `only_fixed` (optional, defaults to `False`):
        Only return fixed timezones
    """
    global _updated_all_tzs, _updated_us_tzs

    # We need to update the offsets to ensure they are correct
    # with zoneinfo latest info
    if not _updated_us_tzs:
        _updated_us_tzs = _update_offsets(_defs._US_TIMEZONES)
    if not _updated_all_tzs:
        _updated_all_tzs = _update_offsets(_defs._ALL_TIMEZONES)

    if only_us:
        return _updated_us_tzs
    elif only_fixed:
        return _defs._FIXED_OFFSETS
    else:
        return _updated_all_tzs


def get_timezones_dict() -> dict[str, _defs.Timezone]:
    global _ALL_TIMEZONES_DICT
    if _ALL_TIMEZONES_DICT is None:
        _ALL_TIMEZONES_DICT = {tz[1]: tz for tz in get_timezones()}
    return _ALL_TIMEZONES_DICT


_ALL_TIMEZONES_DICT: dict[str, _defs.Timezone] | None = None


def _tz_offset_key(offset):
    # Convert a tz offset to a key that can be used by sort().
    # Since Python can sort tuples in lexicographical order, we just convert it
    # to a tuple.
    if isinstance(offset, tuple):
        offset = offset[0]

    mtch = _RE_TZ_OFFSET.match(offset)
    is_negative, hours, minutes = (
        mtch.group(1) == "-",
        int(mtch.group(2)),
        int(mtch.group(3)),
    )

    if is_negative:
        hours, minutes = -hours, -minutes

    return (hours, minutes)


def _update_offsets(timezone_collection: list[tuple[str, str]]) -> list[_defs.Timezone]:
    new_collection = []

    for name, tz_formatted in timezone_collection:
        new_collection.append(tz_utils.format_tz_by_name(name, tz_formatted))

    return sorted(new_collection, key=_tz_offset_key)
