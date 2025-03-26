import unittest
from datetime import datetime
from xcodex.Util.generate_links import generate_links


class TestGenerateLinks(unittest.TestCase):
    def test_generate_links_single_date(self):
        calendar_list = [datetime(2023, 1, 1)]
        expected_links = [
            "https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/2023"
            "/oco2_GEOS_L3CO2_day_20230101_B10206Ar.nc4"
        ]
        self.assertEqual(generate_links(calendar_list), expected_links)

    def test_generate_links_multiple_dates(self):
        calendar_list = [datetime(2023, 1, 1), datetime(2023, 1, 2)]
        expected_links = [
            "https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/2023"
            "/oco2_GEOS_L3CO2_day_20230101_B10206Ar.nc4",
            "https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/2023"
            "/oco2_GEOS_L3CO2_day_20230102_B10206Ar.nc4"
        ]
        self.assertEqual(generate_links(calendar_list), expected_links)

    def test_generate_links_empty_list(self):
        calendar_list = []
        expected_links = []
        self.assertEqual(generate_links(calendar_list), expected_links)


if __name__ == '__main__':
    unittest.main()
