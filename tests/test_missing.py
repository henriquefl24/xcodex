import unittest
import os
import sys
import io
from pandas import DataFrame
from xcodex.Util.missing import new_subset


class TestNewSubset(unittest.TestCase):
    def setUp(self):
        # Mock DataFrame with NaN values in 'XCO2' column
        self.mock_df = DataFrame({
            'location': ['CityA', 'CityB'],
            'jd': [2459580.5, 2459581.5],
            'day': [1, 2],
            'month': [1, 1],
            'year': [2023, 2023],
            'lat': [0.0, 1.0],
            'lon': [0.0, 1.0],
            'lat_index': [0, 1],
            'lon_index': [0, 1],
            'XCO2': [None, 401.0],
            'XCO2_prec': [0.1, 0.2]
        })

    def test_new_subset(self):
        # Suppress stdout and stderr
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        sys_stderr = sys.stderr
        sys.stdout = captured_output
        sys.stderr = captured_output

        try:
            # Call the function
            new_subset(self.mock_df)

            # Check if the file is created in the 'outputs' directory
            output_dir = os.path.join(os.getcwd(), "outputs")
            path_to_file = os.path.join(output_dir, 'new_subset.txt')
            self.assertTrue(os.path.exists(path_to_file))

            # Read the file and check its content
            with open(path_to_file, 'r') as f:
                content = f.read().strip()
                expected_link = ("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/2023"
                                 "/oco2_GEOS_L3CO2_day_20230101_B10206Ar.nc4")
                self.assertIn(expected_link, content)
        finally:
            # Restore stdout and stderr
            sys.stdout = sys_stdout
            sys.stderr = sys_stderr

    def tearDown(self):
        # Clean up the created file
        output_dir = os.path.join(os.getcwd(), "outputs")
        path_to_file = os.path.join(output_dir, 'new_subset.txt')
        if os.path.exists(path_to_file):
            os.remove(path_to_file)


if __name__ == '__main__':
    unittest.main()