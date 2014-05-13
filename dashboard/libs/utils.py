import re
import datetime

from babel.dates import (format_date as babel_format_date,
                         format_time as babel_format_time)
from pyramid.i18n import TranslationStringFactory, get_localizer


translation_string_factory = TranslationStringFactory('Dashboard')
TIMEZONE_RE = re.compile(r'\+.+$')


def remove_time_zone(date_string):
    return TIMEZONE_RE.sub('', date_string)


def date_string_to_date(date_string):
    # strip out the timezone i.e. +03[00]
    date_string = remove_time_zone(date_string)
    return datetime.datetime.strptime(
        date_string, '%Y-%m-%dT%H:%M:%S.%f').date()


def date_string_to_time(date_string):
    # strip out the timezone i.e. +03[00]
    date_string = remove_time_zone(date_string)
    return datetime.datetime.strptime(
        date_string, '%Y-%m-%dT%H:%M:%S.%f').time()


def tuple_to_dict_list(key_tuple, value_tuples):
    return [dict(zip(key_tuple, c)) for c in value_tuples]


def format_date(value, request, date_format='long'):
    localizer = get_localizer(request)
    return babel_format_date(value, date_format, locale=localizer.locale_name)


def format_time(value, request, time_format='short'):
    localizer = get_localizer(request)
    return babel_format_time(value, time_format, locale=localizer.locale_name)