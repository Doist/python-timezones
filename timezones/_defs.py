Timezone = tuple[
    str,  # offset
    str,  # timezone name
    str,  # formatted name
]

_US_TIMEZONES = [
    ("US/Hawaii", "Hawaii"),
    ("US/Alaska", "Alaska"),
    ("US/Pacific", "Pacific Time (US & Canada)"),
    ("US/Arizona", "Arizona"),
    ("US/Mountain", "Mountain Time (US & Canada)"),
    ("US/Central", "Central Time (US & Canada)"),
    ("US/Eastern", "Eastern Time (US & Canada)"),
    ("US/East-Indiana", "Indiana (East)"),
]

_ALL_TIMEZONES = [
    # -11
    ("Pacific/Midway", "International Date Line West"),
    ("Pacific/Midway", "Midway Island"),
    ("Pacific/Samoa", "Samoa"),
    # -10
    ("US/Hawaii", "Hawaii"),
    # -09
    ("US/Alaska", "Alaska"),
    # -08
    ("US/Pacific", "Pacific Time (US & Canada)"),
    ("America/Tijuana", "Tijuana"),
    # -07
    ("US/Arizona", "Arizona"),
    ("America/Mazatlan", "Mazatlan"),
    ("US/Mountain", "Mountain Time (US & Canada)"),
    # -06
    ("America/Chihuahua", "Chihuahua"),
    ("US/Central", "Central Time (US & Canada)"),
    ("Canada/Central", "Central America"),
    ("Canada/Central", "Central Time (US & Canada)"),
    ("Mexico/General", "Guadalajara"),
    ("Mexico/General", "Mexico City"),
    ("America/Monterrey", "Monterrey"),
    ("Canada/Saskatchewan", "Saskatchewan"),
    # -05
    ("America/Bogota", "Bogota"),
    ("US/Eastern", "Eastern Time (US & Canada)"),
    ("US/East-Indiana", "Indiana (East)"),
    ("America/Lima", "Lima"),
    ("America/Rio_Branco", "Rio Branco"),
    ("Etc/GMT+5", "Quito"),  # "plus" value is correct!
    # -04
    ("America/Caracas", "Caracas"),
    ("Canada/Atlantic", "Atlantic Time (Canada)"),
    ("Etc/GMT+4", "La Paz"),  # correct as well
    ("America/Cuiaba", "Cuiaba"),
    ("America/Manaus", "Manaus"),
    ("America/Santiago", "Santiago"),
    ("America/Cuiaba", "Mato Grosso"),
    ("America/Guyana", "Georgetown"),
    # -03
    ("Canada/Newfoundland", "Newfoundland"),
    ("America/Argentina/Buenos_Aires", "Buenos Aires"),
    ("America/Godthab", "Greenland"),
    ("America/Fortaleza", "NE Brazil, Fortaleza"),
    ("America/Sao_Paulo", "Brasilia, Sao Paulo"),
    # -02
    ("America/Noronha", "Fernando de Noronha"),
    # -01
    ("Atlantic/Azores", "Azores"),
    ("Atlantic/Cape_Verde", "Cape Verde Is. "),
    # +00
    ("Africa/Casablanca", "Casablanca"),
    ("Europe/Dublin", "Dublin"),
    ("Europe/London", "Edinburgh"),
    ("Europe/Lisbon", "Lisbon"),
    ("Europe/London", "London"),
    ("Africa/Monrovia", "Monrovia"),
    ("UTC", "UTC"),
    # +01
    ("Europe/Amsterdam", "Amsterdam"),
    ("Europe/Belgrade", "Belgrade"),
    ("Europe/Berlin", "Berlin"),
    ("Europe/Zurich", "Bern"),
    ("Europe/Bratislava", "Bratislava"),
    ("Europe/Brussels", "Brussels"),
    ("Europe/Budapest", "Budapest"),
    ("Europe/Copenhagen", "Copenhagen"),
    ("Europe/Ljubljana", "Ljubljana"),
    ("Europe/Madrid", "Madrid"),
    ("Europe/Oslo", "Oslo"),
    ("Europe/Paris", "Paris"),
    ("Europe/Prague", "Prague"),
    ("Europe/Rome", "Rome"),
    ("Europe/Sarajevo", "Sarajevo"),
    ("Europe/Skopje", "Skopje"),
    ("Europe/Stockholm", "Stockholm"),
    ("Europe/Vienna", "Vienna"),
    ("Europe/Warsaw", "Warsaw"),
    ("Europe/Zagreb", "Zagreb"),
    # +02
    ("Europe/Athens", "Athens"),
    ("Europe/Bucharest", "Bucharest"),
    ("Africa/Cairo", "Cairo"),
    ("Africa/Harare", "Harare"),
    ("Europe/Helsinki", "Helsinki"),
    ("Asia/Jerusalem", "Jerusalem"),
    ("Europe/Kyiv", "Kyiv"),
    ("Africa/Johannesburg", "Pretoria"),
    ("Europe/Riga", "Riga"),
    ("Europe/Sofia", "Sofia"),
    ("Europe/Tallinn", "Tallinn"),
    ("Europe/Vilnius", "Vilnius"),
    # +03
    ("Asia/Baghdad", "Baghdad"),
    ("Asia/Kuwait", "Kuwait"),
    ("Europe/Istanbul", "Istanbul"),
    ("Europe/Minsk", "Minsk"),
    ("Europe/Moscow", "Moscow"),
    ("Africa/Nairobi", "Nairobi"),
    ("Asia/Riyadh", "Riyadh"),
    ("Europe/Moscow", "St. Petersburg"),
    ("Europe/Volgograd", "Volgograd"),
    ("Asia/Tehran", "Tehran"),
    # +04
    ("Asia/Dubai", "Abu Dhabi"),
    ("Asia/Baku", "Baku"),
    ("Asia/Muscat", "Muscat"),
    ("Asia/Tbilisi", "Tbilisi"),
    ("Asia/Yerevan", "Yerevan"),
    ("Asia/Kabul", "Kabul"),
    # +05
    ("Asia/Karachi", "Islamabad"),
    ("Asia/Karachi", "Karachi"),
    ("Asia/Tashkent", "Tashkent"),
    # Note that different locations match the same timezone name
    # and the location which gives the name to the timezone
    # comes last. It's to ensure that the function
    # html_render_timezones(..., current_selected='Asia/Calcutta')
    # takes "most sensible" timezone name.
    ("Asia/Calcutta", "Chennai"),
    ("Asia/Calcutta", "Mumbai"),
    ("Asia/Calcutta", "New Delhi"),
    ("Asia/Calcutta", "Sri Jayawardenepura"),
    ("Asia/Calcutta", "Kolkata"),
    ("Asia/Kathmandu", "Kathmandu"),
    # +06
    ("Asia/Almaty", "Almaty"),
    ("Asia/Almaty", "Astana"),
    ("Asia/Dhaka", "Dhaka"),
    ("Asia/Urumqi", "Urumqi"),
    ("Asia/Rangoon", "Rangoon"),
    # +07
    ("Asia/Novosibirsk", "Novosibirsk"),
    ("Asia/Bangkok", "Bangkok"),
    ("Asia/Saigon", "Hanoi"),
    ("Asia/Jakarta", "Jakarta"),
    ("Asia/Krasnoyarsk", "Krasnoyarsk"),
    # +08
    ("Asia/Harbin", "Beijing"),
    ("Asia/Chongqing", "Chongqing"),
    ("Asia/Hong_Kong", "Hong Kong"),
    ("Asia/Irkutsk", "Irkutsk"),
    ("Asia/Kuala_Lumpur", "Kuala Lumpur"),
    ("Australia/Perth", "Perth"),
    ("Singapore", "Singapore"),
    ("Asia/Ulaanbaatar", "Ulaanbaatar"),
    ("Asia/Taipei", "Taipei"),
    # +09
    ("Asia/Seoul", "Seoul"),
    ("Asia/Tokyo", "Tokyo"),
    ("Asia/Yakutsk", "Yakutsk"),
    ("Australia/Adelaide", "Adelaide"),
    ("Australia/Darwin", "Darwin"),
    # +10
    ("Australia/Brisbane", "Brisbane"),
    ("Australia/Canberra", "Canberra"),
    ("Pacific/Guam", "Guam"),
    ("Australia/Hobart", "Hobart"),
    ("Australia/Melbourne", "Melbourne"),
    ("Pacific/Port_Moresby", "Port Moresby"),
    ("Australia/Sydney", "Sydney"),
    ("Asia/Vladivostok", "Vladivostok"),
    # +11
    ("Asia/Magadan", "Magadan"),
    ("Pacific/Noumea", "New Caledonia"),
    ("Pacific/Guadalcanal", "Solomon Is. "),
    ("Pacific/Norfolk", "Norfolk"),
    # +12
    ("Pacific/Auckland", "Auckland"),
    ("Pacific/Fiji", "Fiji"),
    ("Asia/Kamchatka", "Kamchatka"),
    ("Asia/Kamchatka", "Marshall Is."),
    ("Pacific/Auckland", "Wellington"),
    # +13
    ("Pacific/Tongatapu", "Nuku'alofa"),
]

_TZ_ALIASES = {
    "Europe/Kyiv": "Europe/Kiev",
}

_FIXED_OFFSETS: list[Timezone] = [
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
    ("+1300", "GMT +13:00", "GMT +13:00"),
]
