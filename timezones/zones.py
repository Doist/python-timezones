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

from future.backports import cmp_to_key
from past.builtins import cmp
from timezones import tz_utils

_UPDATED_TZS = False


def get_timezones(only_us=False, only_fixed=False):
    """Returns an iterator of timezones.

    `only_us` (optional, defaults to `False`):
        Only return US related timezones

    `only_fixed` (optional, defaults to `False`):
        Only return fixed timezones
    """
    global _US_TIMEZONES, _ALL_TIMEZONES, _UPDATED_TZS

    # We need to update the offsets to ensure they are correct
    # with pytz latest info
    if not _UPDATED_TZS:
        _US_TIMEZONES = _update_offests(_US_TIMEZONES)
        _ALL_TIMEZONES = _update_offests(_ALL_TIMEZONES)
        _UPDATED_TZS = True

    if only_us:
        for tz in _US_TIMEZONES:
            yield tz
    elif only_fixed:
        for tz in _FIXED_OFFSETS:
            yield tz
    else:
        for tz in _ALL_TIMEZONES:
            yield tz


def get_timezones_dict():
    global _ALL_TIMEZONES_DICT
    if _ALL_TIMEZONES_DICT is None:
        _ALL_TIMEZONES_DICT = {tz[1]: tz for tz in get_timezones()}
    return _ALL_TIMEZONES_DICT


# --- Definitions ----------------------------------------------
_US_TIMEZONES = [
    ("-1000", "US/Hawaii", '(GMT-1000) Hawaii'),
    ("-0900", "US/Alaska", '(GMT-0900) Alaska'),
    ("-0800", "US/Pacific", '(GMT-0800) Pacific Time (US & Canada)'),
    ("-0700", "US/Arizona", '(GMT-0700) Arizona'),
    ("-0700", "US/Mountain", '(GMT-0700) Mountain Time (US & Canada)'),
    ("-0600", "US/Central", '(GMT-0600) Central Time (US & Canada)'),
    ("-0500", "US/Eastern", '(GMT-0500) Eastern Time (US & Canada)'),
    ("-0500", "US/East-Indiana", '(GMT-0500) Indiana (East)'),
]

_ALL_TIMEZONES = [
    ("-1100", "Pacific/Midway", '(GMT-1100) International Date Line West'),
    ("-1100", "Pacific/Midway", '(GMT-1100) Midway Island'),
    ("-1100", "Pacific/Samoa", '(GMT-1100) Samoa'),
    ("-1000", "US/Hawaii", '(GMT-1000) Hawaii'),
    ("-0900", "US/Alaska", '(GMT-0900) Alaska'),
    ("-0800", "US/Pacific", '(GMT-0800) Pacific Time (US & Canada)'),
    ("-0800", "America/Tijuana", '(GMT-0800) Tijuana'),
    ("-0700", "US/Arizona", '(GMT-0700) Arizona'),
    ("-0700", "America/Chihuahua", '(GMT-0700) Chihuahua'),
    ("-0700", "America/Mazatlan", '(GMT-0700) Mazatlan'),
    ("-0700", "US/Mountain", '(GMT-0700) Mountain Time (US & Canada)'),
    ("-0600", "US/Central", '(GMT-0600) Central Time (US & Canada)'),
    ("-0600", "Canada/Central", '(GMT-0600) Central America'),
    ("-0600", "Canada/Central", '(GMT-0600) Central Time (US & Canada)'),
    ("-0600", "Mexico/General", '(GMT-0600) Guadalajara'),
    ("-0600", "Mexico/General", '(GMT-0600) Mexico City'),
    ("-0600", "America/Monterrey", '(GMT-0600) Monterrey'),
    ("-0600", "Canada/Saskatchewan", '(GMT-0600) Saskatchewan'),
    ("-0500", "America/Bogota", '(GMT-0500) Bogota'),
    ("-0500", "US/Eastern", '(GMT-0500) Eastern Time (US & Canada)'),
    ("-0500", "US/East-Indiana", '(GMT-0500) Indiana (East)'),
    ("-0500", "America/Lima", '(GMT-0500) Lima'),
    ("-0500", "America/Rio_Branco", '(GMT-0500) Rio Branco'),
    ("-0500", "Etc/GMT+5", '(GMT-0500) Quito'),  # "plus" value is correct!
    ("-0400", "America/Caracas", '(GMT-0400) Caracas'),
    ("-0400", "Canada/Atlantic", '(GMT-0400) Atlantic Time (Canada)'),
    ("-0400", "Etc/GMT+4", '(GMT-0400) La Paz'),  # correct as well
    ("-0400", "America/Cuiaba", '(GMT-0400) Cuiaba'),
    ("-0400", "America/Manaus", '(GMT-0400) Manaus'),
    ("-0400", "America/Santiago", '(GMT-0400) Santiago'),
    ("-0400", "America/Cuiaba", '(GMT-0400) Mato Grosso'),
    ("-0330", "Canada/Newfoundland", '(GMT-0330) Newfoundland'),
    ("-0300", "America/Argentina/Buenos_Aires", '(GMT-0300) Buenos Aires'),
    ("-0400", "America/Guyana", '(GMT-0400) Georgetown'),
    ("-0300", "America/Godthab", '(GMT-0300) Greenland'),
    ("-0300", "America/Fortaleza", '(GMT-0300) NE Brazil, Fortaleza'),
    ("-0300", "America/Sao_Paulo", '(GMT-0300) Brasilia, Sao Paulo'),
    ("-0200", "America/Noronha", '(GMT-0200) Fernando de Noronha'),
    ("-0100", "Atlantic/Azores", '(GMT-0100) Azores'),
    ("-0100", "Atlantic/Cape_Verde", '(GMT-0100) Cape Verde Is. '),
    ("+0100", "Africa/Casablanca", '(GMT+0100) Casablanca'),
    ("+0100", "Europe/Dublin", '(GMT+0100) Dublin'),
    ("+0000", "Europe/London", '(GMT+0000) Edinburgh'),
    ("+0000", "Europe/Lisbon", '(GMT+0000) Lisbon'),
    ("+0000", "Europe/London", '(GMT+0000) London'),
    ("+0000", "Africa/Monrovia", '(GMT+0000) Monrovia'),
    ("+0000", "UTC", '(GMT+0000) UTC'),
    ("+0100", "Europe/Amsterdam", '(GMT+0100) Amsterdam'),
    ("+0100", "Europe/Belgrade", '(GMT+0100) Belgrade'),
    ("+0100", "Europe/Berlin", '(GMT+0100) Berlin'),
    ("+0100", "Europe/Zurich", '(GMT+0100) Bern'),
    ("+0100", "Europe/Bratislava", '(GMT+0100) Bratislava'),
    ("+0100", "Europe/Brussels", '(GMT+0100) Brussels'),
    ("+0100", "Europe/Budapest", '(GMT+0100) Budapest'),
    ("+0100", "Europe/Copenhagen", '(GMT+0100) Copenhagen'),
    ("+0100", "Europe/Ljubljana", '(GMT+0100) Ljubljana'),
    ("+0100", "Europe/Madrid", '(GMT+0100) Madrid'),
    ("+0100", "Europe/Paris", '(GMT+0100) Paris'),
    ("+0100", "Europe/Prague", '(GMT+0100) Prague'),
    ("+0100", "Europe/Rome", '(GMT+0100) Rome'),
    ("+0100", "Europe/Sarajevo", '(GMT+0100) Sarajevo'),
    ("+0100", "Europe/Skopje", '(GMT+0100) Skopje'),
    ("+0100", "Europe/Stockholm", '(GMT+0100) Stockholm'),
    ("+0100", "Europe/Vienna", '(GMT+0100) Vienna'),
    ("+0100", "Europe/Warsaw", '(GMT+0100) Warsaw'),
    ("+0100", "Europe/Zagreb", '(GMT+0100) Zagreb'),
    ("+0200", "Europe/Athens", '(GMT+0200) Athens'),
    ("+0200", "Europe/Bucharest", '(GMT+0200) Bucharest'),
    ("+0200", "Africa/Cairo", '(GMT+0200) Cairo'),
    ("+0200", "Africa/Harare", '(GMT+0200) Harare'),
    ("+0200", "Europe/Helsinki", '(GMT+0200) Helsinki'),
    ("+0300", "Europe/Istanbul", '(GMT+0300) Istanbul'),
    ("+0200", "Asia/Jerusalem", '(GMT+0200) Jerusalem'),
    ("+0200", "Europe/Kiev", '(GMT+0200) Kyiv'),
    ("+0300", "Europe/Minsk", '(GMT+0300) Minsk'),
    ("+0200", "Africa/Johannesburg", '(GMT+0200) Pretoria'),
    ("+0200", "Europe/Riga", '(GMT+0200) Riga'),
    ("+0200", "Europe/Sofia", '(GMT+0200) Sofia'),
    ("+0200", "Europe/Tallinn", '(GMT+0200) Tallinn'),
    ("+0200", "Europe/Vilnius", '(GMT+0200) Vilnius'),
    ("+0300", "Asia/Baghdad", '(GMT+0300) Baghdad'),
    ("+0300", "Asia/Kuwait", '(GMT+0300) Kuwait'),
    ("+0300", "Europe/Moscow", '(GMT+0300) Moscow'),
    ("+0300", "Africa/Nairobi", '(GMT+0300) Nairobi'),
    ("+0300", "Asia/Riyadh", '(GMT+0300) Riyadh'),
    ("+0300", "Europe/Moscow", '(GMT+0300) St. Petersburg'),
    ("+0400", "Europe/Volgograd", '(GMT+0400) Volgograd'),
    ("+0330", "Asia/Tehran", '(GMT+0330) Tehran'),
    ("+0400", "Asia/Dubai", '(GMT+0400) Abu Dhabi'),
    ("+0400", "Asia/Baku", '(GMT+0400) Baku'),
    ("+0400", "Asia/Muscat", '(GMT+0400) Muscat'),
    ("+0400", "Asia/Tbilisi", '(GMT+0400) Tbilisi'),
    ("+0400", "Asia/Yerevan", '(GMT+0400) Yerevan'),
    ("+0430", "Asia/Kabul", '(GMT+0430) Kabul'),
    ("+0500", "Asia/Karachi", '(GMT+0500) Islamabad'),
    ("+0500", "Asia/Karachi", '(GMT+0500) Karachi'),
    ("+0500", "Asia/Tashkent", '(GMT+0500) Tashkent'),

    # Note that different locations match the same timezone name
    # and the location which gives the name to the timezone
    # comes last. It's to ensure that the function
    # html_render_timezones(..., current_selected='Asia/Calcutta')
    # takes "most sensible" timezone name.
    ("+0530", "Asia/Calcutta", '(GMT+0530) Chennai'),
    ("+0530", "Asia/Calcutta", '(GMT+0530) Mumbai'),
    ("+0530", "Asia/Calcutta", '(GMT+0530) New Delhi'),
    ("+0530", "Asia/Calcutta", '(GMT+0530) Sri Jayawardenepura'),
    ("+0530", "Asia/Calcutta", '(GMT+0530) Kolkata'),
    ("+0545", "Asia/Kathmandu", '(GMT+0545) Kathmandu'),
    ("+0600", "Asia/Almaty", '(GMT+0600) Almaty'),
    ("+0600", "Asia/Almaty", '(GMT+0600) Astana'),
    ("+0600", "Asia/Dhaka", '(GMT+0600) Dhaka'),
    ("+0600", "Asia/Urumqi", '(GMT+0600) Urumqi'),
    ("+0700", "Asia/Novosibirsk", '(GMT+0700) Novosibirsk'),
    ("+0630", "Asia/Rangoon", '(GMT+0630) Rangoon'),
    ("+0700", "Asia/Bangkok", '(GMT+0700) Bangkok'),
    ("+0700", "Asia/Saigon", '(GMT+0700) Hanoi'),
    ("+0700", "Asia/Jakarta", '(GMT+0700) Jakarta'),
    ("+0700", "Asia/Krasnoyarsk", '(GMT+0700) Krasnoyarsk'),
    ("+0800", "Asia/Harbin", '(GMT+0800) Beijing'),
    ("+0800", "Asia/Chongqing", '(GMT+0800) Chongqing'),
    ("+0800", "Asia/Hong_Kong", '(GMT+0800) Hong Kong'),
    ("+0800", "Asia/Irkutsk", '(GMT+0800) Irkutsk'),
    ("+0800", "Asia/Kuala_Lumpur", '(GMT+0800) Kuala Lumpur'),
    ("+0800", "Australia/Perth", '(GMT+0800) Perth'),
    ("+0800", "Singapore", '(GMT+0800) Singapore'),
    ("+0800", "Asia/Taipei", '(GMT+0800) Taipei'),
    ("+0800", "Asia/Taipei", '(GMT+0800) Ulaan Bataar'),
    ("+0900", "Asia/Seoul", '(GMT+0900) Seoul'),
    ("+0900", "Asia/Tokyo", '(GMT+0900) Tokyo'),
    ("+0900", "Asia/Yakutsk", '(GMT+0900) Yakutsk'),
    ("+0930", "Australia/Adelaide", '(GMT+0930) Adelaide'),
    ("+0930", "Australia/Darwin", '(GMT+0930) Darwin'),
    ("+1000", "Australia/Brisbane", '(GMT+1000) Brisbane'),
    ("+1000", "Australia/Canberra", '(GMT+1000) Canberra'),
    ("+1000", "Pacific/Guam", '(GMT+1000) Guam'),
    ("+1000", "Australia/Hobart", '(GMT+1000) Hobart'),
    ("+1000", "Australia/Melbourne", '(GMT+1000) Melbourne'),
    ("+1000", "Pacific/Port_Moresby", '(GMT+1000) Port Moresby'),
    ("+1000", "Australia/Sydney", '(GMT+1000) Sydney'),
    ("+1000", "Asia/Vladivostok", '(GMT+1000) Vladivostok'),
    ("+1100", "Asia/Magadan", '(GMT+1100) Magadan'),
    ("+1100", "Pacific/Noumea", '(GMT+1100) New Caledonia'),
    ("+1100", "Pacific/Guadalcanal", '(GMT+1100) Solomon Is. '),
    ("+1100", "Pacific/Norfolk", '(GMT+1100) Norfolk'),
    ("+1200", "Pacific/Auckland", '(GMT+1200) Auckland'),
    ("+1200", "Pacific/Fiji", '(GMT+1200) Fiji'),
    ("+1200", "Asia/Kamchatka", '(GMT+1200) Kamchatka'),
    ("+1200", "Asia/Kamchatka", '(GMT+1200) Marshall Is.'),
    ("+1200", "Pacific/Auckland", '(GMT+1200) Wellington'),
    ("+1300", "Pacific/Tongatapu", "(GMT+1300) Nuku'alofa")
]

# yapf: disable
_FIXED_OFFSETS = [
        ("-1200", "GMT -12:00", "GMT -12:00"),
        ("-1100", "GMT -11:00", "GMT -11:00"),
        ("-1000", "GMT -10:00", "GMT -10:00"),
        ("-0900", "GMT -9:00", "GMT -9:00"),
        ("-0800", "GMT -8:00", "GMT -8:00"),
        ("-0700", "GMT -7:00", "GMT -7:00"),
        ("-0600", "GMT -6:00", "GMT -6:00"),
        ("-0500", "GMT -5:00", "GMT -5:00"),
        ("-0400", "GMT -4:00", "GMT -4:00"),
        ("-0300", "GMT -3:00", "GMT -3:00"),
        ("-0200", "GMT -2:00", "GMT -2:00"),
        ("-0100", "GMT -1:00", "GMT -1:00"),
        ("+0000", "GMT", "GMT"),
        ("+0000", "UTC", "UTC"),
        ("+0100", "GMT +1:00", "GMT +1:00"),
        ("+0200", "GMT +2:00", "GMT +2:00"),
        ("+0300", "GMT +3:00", "GMT +3:00"),
        ("+0400", "GMT +4:00", "GMT +4:00"),
        ("+0500", "GMT +5:00", "GMT +5:00"),
        ("+0600", "GMT +6:00", "GMT +6:00"),
        ("+0700", "GMT +7:00", "GMT +7:00"),
        ("+0800", "GMT +8:00", "GMT +8:00"),
        ("+0900", "GMT +9:00", "GMT +9:00"),
        ("+1000", "GMT +10:00", "GMT +10:00"),
        ("+1100", "GMT +11:00", "GMT +11:00"),
        ("+1200", "GMT +12:00", "GMT +12:00"),
        ("+1300", "GMT +13:00", "GMT +13:00")
]
# yapf: enable

_ALL_TIMEZONES_DICT = None


def _sort_by_tzoffset(a_offset, b_offset):
    # Transform if it's a tuple
    if isinstance(a_offset, tuple):
        a_offset = a_offset[0]
        b_offset = b_offset[0]

    def split(offset):
        match = re.match(r'([+-])(\d\d)(\d\d)', offset)
        return match.group(1) == '-', int(match.group(2)), int(match.group(3))

    a_negative, a_hours, a_minutes = split(a_offset)
    b_negative, b_hours, b_minutes = split(b_offset)

    if a_hours == 0 and b_hours != 0:
        return 1

    if a_negative and not b_negative:
        return -1

    if not a_negative and b_negative:
        return 1

    if a_negative and b_negative:
        a_hours = -1 * a_hours
        b_hours = -1 * b_hours

    if a_hours > b_hours:
        return 1
    elif a_hours == b_hours:
        return cmp(a_minutes, b_minutes)
    else:
        return -1


def _update_offests(timezone_collection):
    new_collection = []

    for tz_offset, name, tz_formated in timezone_collection:
        new_collection.append(tz_utils.format_tz_by_name(name, tz_formated))

    return sorted(new_collection, key=cmp_to_key(_sort_by_tzoffset))
