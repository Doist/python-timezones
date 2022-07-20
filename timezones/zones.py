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
import re

from timezones import tz_utils, _defs

_UPDATED_TZS = False

_RE_TZ_OFFSET = re.compile(r"([+-])(\d\d)(\d\d)")


def get_timezones(only_us=False, only_fixed=False):
    """Returns an iterator of timezones.

    `only_us` (optional, defaults to `False`):
        Only return US related timezones

    `only_fixed` (optional, defaults to `False`):
        Only return fixed timezones
    """
    global _UPDATED_TZS

    # We need to update the offsets to ensure they are correct
    # with pytz latest info
    if not _UPDATED_TZS:
        _US_TIMEZONES = _update_offsets(_defs._US_TIMEZONES)
        _ALL_TIMEZONES = _update_offsets(_defs._ALL_TIMEZONES)
        _UPDATED_TZS = True

    if only_us:
        for tz in _defs._US_TIMEZONES:
            yield tz
    elif only_fixed:
        for tz in _defs._FIXED_OFFSETS:
            yield tz
    else:
        for tz in _defs._ALL_TIMEZONES:
            yield tz


def get_timezones_dict():
    global _ALL_TIMEZONES_DICT
    if _ALL_TIMEZONES_DICT is None:
        _ALL_TIMEZONES_DICT = {tz[1]: tz for tz in get_timezones()}
    return _ALL_TIMEZONES_DICT



_ALL_TIMEZONES_DICT = None


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


def _update_offsets(timezone_collection):
    new_collection = []

    for _, name, tz_formated in timezone_collection:
        new_collection.append(tz_utils.format_tz_by_name(name, tz_formated))

    return sorted(new_collection, key=_tz_offset_key)
