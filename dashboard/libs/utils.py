import re
import datetime

from babel.dates import (format_date as babel_format_date,
                         format_time as babel_format_time)
from babel.numbers import (format_decimal as babel_format_decimal,
                           format_percent as babel_format_percent)
from pyramid.i18n import TranslationStringFactory, get_localizer


translation_string_factory = TranslationStringFactory('Dashboard')
TIMEZONE_RE = re.compile(r'\+.+$')
default_date_format = '%Y-%m-%dT%H:%M:%S.%f'


def remove_time_zone(date_string):
    return TIMEZONE_RE.sub('', date_string)


def date_string_to_datetime(date_string, date_format=default_date_format):
    # strip out the timezone i.e. +03[00]
    date_string = remove_time_zone(date_string)
    return datetime.datetime.strptime(
        date_string, date_format)


def date_string_to_date(date_string, date_format=default_date_format):
    return date_string_to_datetime(date_string, date_format).date()


def date_string_to_time(date_string, date_format=default_date_format):
    return date_string_to_datetime(date_string, date_format).time()


def date_string_to_month(date_string, date_format=default_date_format):
    """
    Set the date to the first day of the month
    """
    date = date_string_to_datetime(date_string, date_format)
    return datetime.date(date.year, date.month, 01)


def tuple_to_dict_list(key_tuple, value_tuples):
    return [dict(zip(key_tuple, c)) for c in value_tuples]


def format_date(value, request, date_format='long'):
    localizer = get_localizer(request)
    return babel_format_date(value, date_format, locale=localizer.locale_name)


def format_time(value, request, time_format='short'):
    localizer = get_localizer(request)
    return babel_format_time(value, time_format, locale=localizer.locale_name)


def format_decimal(value, request, number_format='#,##0.###;-#'):
    localizer = get_localizer(request)
    return babel_format_decimal(
        value, format=number_format, locale=localizer.locale_name)


def format_percent(value, request, percent_format='#,##0.##%;-#'):
    localizer = get_localizer(request)
    return babel_format_percent(
        value, format=percent_format, locale=localizer.locale_name)