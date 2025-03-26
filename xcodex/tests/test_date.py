import unittest
from xcodex.Util.date import calendar_days
from pandas import Timestamp


class TestCalendarDays(unittest.TestCase):
    def test_valid_date_range(self):
        start = "1st of January, 2015"
        end = "31st of January, 2021"
        result = calendar_days(start, end)
        expected_start = Timestamp('2015-01-01')
        expected_end = Timestamp('2021-01-31')
        self.assertEqual(result[0], expected_start)
        self.assertEqual(result[-1], expected_end)

    def test_invalid_date_format(self):
        start = "invalid date"
        end = "31st of January, 2015"
        result = calendar_days(start, end)
        self.assertIsNone(result)

    def test_leap_year(self):
        start = "28th of February, 2020"
        end = "1st of March, 2020"
        result = calendar_days(start, end)
        expected_dates = [Timestamp('2020-02-28'), Timestamp('2020-02-29'), Timestamp('2020-03-01')]
        self.assertListEqual(list(result), expected_dates)


if __name__ == '__main__':
    unittest.main()
