from django.test import TestCase
from datetime import date

from api.utils.utils import calculate_total_days, get_midpoint_date, is_date_in_range


class UtilsTest(TestCase):
    def test_calculate_total_days(self):
        start_date = date(2024, 7, 1)
        end_date = date(2024, 7, 14)
        self.assertEqual(calculate_total_days(start_date, end_date), 14)

    def test_get_midpoint_date(self):
        start_date = date(2024, 7, 1)
        end_date = date(2024, 7, 14)
        self.assertEqual(get_midpoint_date(start_date, end_date), date(2024, 7, 7))

    def test_is_date_in_range(self):
        start_date = date(2024, 7, 1)
        end_date = date(2024, 7, 14)
        test_date = date(2024, 7, 7)
        self.assertTrue(is_date_in_range(test_date, start_date, end_date))
        self.assertFalse(is_date_in_range(date(2024, 6, 30), start_date, end_date))
