# File: tests/test_make_Dataframe.py

import unittest
from pandas import Series, DataFrame
from xcodex.Util.make_Dataframe import make_dataframe


class TestMakeDataFrame(unittest.TestCase):
    def test_make_dataframe(self):
        # Mock data
        city = Series(["CityA", "CityB"])
        jd = Series([2459580.5, 2459581.5])
        day = Series([1, 2])
        month = Series([1, 1])
        year = Series([2023, 2023])
        lat = Series([0.0, 1.0])
        lon = Series([0.0, 1.0])
        lat_grid = Series([0, 1])
        lon_grid = Series([0, 1])
        XCO2_values = Series([400.0, 401.0])
        XCO2PREC_values = Series([0.1, 0.2])

        # Call the function
        df = make_dataframe(city, jd, day, month, year, lat, lon, lat_grid, lon_grid, XCO2_values, XCO2PREC_values)

        # Expected DataFrame
        expected_df = DataFrame({
            'location': city,
            'jd': jd,
            'day': day,
            'month': month,
            'year': year,
            'lat': lat,
            'lon': lon,
            'lat_grid': lat_grid,
            'lon_grid': lon_grid,
            'XCO2': XCO2_values,
            'XCO2PREC': XCO2PREC_values
        }).sort_values(by=['location', 'year']).reset_index(drop=True)

        # Assertions
        self.assertTrue(df.equals(expected_df))


if __name__ == '__main__':
    unittest.main()
