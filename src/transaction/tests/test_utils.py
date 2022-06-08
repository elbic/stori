from transaction.utils import get_month_name_from_number
from django.test import TestCase
import datetime


class UtilsTest(TestCase):
    def setUp(self):
        pass

    def test_get_month_name_from_number(self):
        for month in range(1, 12):
            assert get_month_name_from_number(month) == datetime.date(
                1900, month, 1
            ).strftime("%B")
