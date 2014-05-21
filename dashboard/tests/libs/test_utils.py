import unittest
import datetime

from pyramid import testing

from dashboard.libs import utils


class TestUtils(unittest.TestCase):
    def test_remove_time_zone_if_exists(self):
        result = utils.remove_time_zone('2014-04-29T10:35:00.000+03')
        self.assertEqual(result, '2014-04-29T10:35:00.000')

    def test_remove_time_zone_if_not_exists(self):
        result = utils.remove_time_zone('2014-04-29T10:35:00.000')
        self.assertEqual(result, '2014-04-29T10:35:00.000')

    def test_date_string_to_datetime(self):
        date_string = '2014-04-29T10:35:00.000+03'
        result = utils.date_string_to_datetime(date_string)
        self.assertEqual(datetime.datetime(2014, 04, 29, 10, 35), result)

    def test_date_string_to_date(self):
        date_string = '2014-04-29T10:35:00.000+03'
        result = utils.date_string_to_date(date_string)
        self.assertEqual(datetime.date(2014, 04, 29), result)

    def test_date_string_to_time(self):
        date_string = '2014-04-29T10:35:00.000+03'
        result = utils.date_string_to_time(date_string)
        self.assertEqual(datetime.time(10, 35, 00), result)

    def test_date_string_to_month(self):
        date_string = '2014-04-29T10:35:00.000+03'
        result = utils.date_string_to_month(date_string)
        self.assertEqual(datetime.date(2014, 04, 01), result)

    def test_format_date(self):
        value = datetime.date(2014, 04, 03)
        request = testing.DummyRequest()
        result = utils.format_date(value, request)
        self.assertEqual(result, 'April 3, 2014')

    def test_format_time(self):
        value = datetime.time(13, 15, 03)
        request = testing.DummyRequest()
        result = utils.format_time(value, request)
        self.assertEqual(result, '1:15 PM')

    def test_format_decimal(self):
        value = 0.123632
        request = testing.DummyRequest()
        result = utils.format_decimal(value, request)
        self.assertEqual(result, '0.124')