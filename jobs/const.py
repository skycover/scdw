# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def __get_currenttz():
    """ get current timezone """
    from sys import platform
    import pytz
    if platform == 'cygwin':
        from subprocess import check_output
        tz_str = check_output('tzset')
    else:
        f = open('/etc/timezone', 'r')
        tz_str = f.readline()
    tz = pytz.timezone(tz_str.replace('\n', ''))
    return tz


def __get_utc_suffix():
    from datetime import datetime
    tz = __get_currenttz()
    now = datetime.now(tz)
    return '{firstpart}:{secondpart}'.format(
        firstpart=now.strftime('%z')[:3],
        secondpart=now.strftime('%z')[3:]
    )

TIMEZONE = __get_currenttz()
UTC_SUFFIX = __get_utc_suffix()
DATEFORMAT_IN_NAME = '%Y%m%dT%H%M%SZ'
DATEFORMAT_FOR_SCDUPY = '%Y-%m-%dT%H:%M:%S' + UTC_SUFFIX
