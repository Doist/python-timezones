"""
tz_rendering
~~~~~~~~

HTML helper to render timezones. The output will be a SELECT element.

Will auto guess the user's timezone based on IP. Will auto-select the current
selected timezone.

Example usage (returns HTML based on current properties)::

    html_timezones = tz_rendering.html_render_timezones(
        'timezone',
        current_selected,
        get_current_ip(),
        first_entry=_('Select your timezone'),
    )

:copyright: 2012 by Amir Salihefendic ( http://amix.dk/ )
:license: MIT
"""
from __future__ import annotations

import json
from typing import Any

from . import _defs, tz_utils, zones


def html_render_timezones(
    select_name: str,
    current_selected: str | None = None,
    user_ip: str | None = None,
    first_entry: str = "Select your timezone",
    force_current_selected: bool = False,
    select_id: Any = None,
    default_timezone: str | None = None,
) -> str:
    """Render timezone and output HTML.

    `select_name`:
        Is the name of the select element, e.g. <select name="%(select_name)s">.

    `current_selected` (optional):
        Is the name of the current timezone, e.g. "Europe/Copenhagen"
        is used to auto select the current timezone option in the select element

    `user_ip` (optional):
        User's ip, used to auto guess the timezone

    `first_entry` (optional):
        What should the first option be? If `None` it won't be shown at all

    `force_current_selected` (optional):
        Force a show in the top of user's current timezone

    `select_id`:
        Select's elements id, e.g. <select id="%(select_id)s">.
    """

    # Makes it possible to only mark one timezone as selected
    sel_checker = {"non_selected_yet": True}

    def render_option(value, name, selected=False):
        if selected and sel_checker["non_selected_yet"]:
            is_selected = 'selected="selected"'
            sel_checker["non_selected_yet"] = False
        else:
            is_selected = ""
        return '<option value="%s" %s>%s</option>' % (value, is_selected, name)

    def render_option_disabled():
        return '<option disabled="disabled">--------------------</option>'

    if select_id:
        select_elm = '<select name="%s" id="%s">' % (select_name, select_id)
    else:
        select_elm = '<select name="%s">' % select_name

    result = [select_elm]

    if first_entry:
        result.append('<option value="">%s</option>' % first_entry)
        result.append(render_option_disabled())

    if force_current_selected and current_selected:
        timezone = format_tz(current_selected)
        if timezone:
            result.append(render_option(timezone[1], timezone[2], True))
            result.append(render_option_disabled())

    # Guess user's timezone by user_ip
    if user_ip:
        gussed_timezone = tz_utils.guess_timezone_by_ip(user_ip)

        if not gussed_timezone and default_timezone:
            gussed_timezone = format_tz(default_timezone)

        if gussed_timezone:
            is_set = current_selected == gussed_timezone[1] or current_selected is None
            result.append(render_option(gussed_timezone[1], gussed_timezone[2], is_set))
            result.append(render_option_disabled())

    for tz in zones.get_timezones(only_us=True):
        result.append(render_option(tz[1], tz[2], current_selected == tz[1]))

    result.append(render_option_disabled())

    for tz in zones.get_timezones():
        result.append(render_option(tz[1], tz[2], current_selected == tz[1]))

    result.append(render_option_disabled())

    for tz in zones.get_timezones(only_fixed=True):
        result.append(render_option(tz[1], tz[2], current_selected == tz[1]))

    result.append("</select>")

    return "\n".join(result)


def get_timezones_json() -> str:
    result = []
    for tz in zones.get_timezones(only_us=True):
        result.append((tz[1], tz[2]))

    for tz in zones.get_timezones():
        result.append((tz[1], tz[2]))

    for tz in zones.get_timezones(only_fixed=True):
        result.append((tz[1], tz[2]))

    return json.dumps(result)


def format_tz(tz_name: str) -> _defs.Timezone:
    tz = zones.get_timezones_dict().get(tz_name)
    if tz:
        return tz
    return tz_utils.format_tz_by_name(tz_name)
