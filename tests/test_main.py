import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from xcodex.main import xco2_extract


class TestMain(unittest.TestCase):

    @patch('xcodex.main.xr.open_dataset')
    @patch('xcodex.main.make_dataframe')
    @patch('xcodex.main.calendar_days')
    @patch('xcodex.main.generate_links')
    @patch('xcodex.main.download')
    def test_xco2_extract(self, mock_download, mock_generate_links, mock_calendar_days, mock_make_dataframe, mock_open_dataset):
        # Mocking the return values
        mock_calendar_days.return_value = [MagicMock()]
        mock_generate_links.return_value = ['mock_link']
        mock_make_dataframe.return_value = DataFrame({
            'location': [],
            'jd': [],
            'day': [],
            'month': [],
            'year': [],
            'lat': [],
            'lon': [],
            'lat_grid': [],
            'lon_grid': [],
            'XCO2': [],
            'XCO2PREC': []
        })  # Ensure all expected columns exist

        # Mocking open_dataset object
        mock_dataset = MagicMock()
        mock_dataset.__getitem__.return_value = MagicMock(begin_date='20150101')
        mock_open_dataset.return_value = mock_dataset

        # Call the function
        location = {'city': [(19.479488, -155.602829), (19.479488, -155.602829)]}  # Example coordinates for Mauna Loa
        result = xco2_extract('01 of January, 2015', '31 of January, 2015', method="requests", output_format="csv", display_variables=['location'], **location)

        # Assertions
        mock_calendar_days.assert_called_once_with('01 of January, 2015', '31 of January, 2015')
        mock_generate_links.assert_called_once()
        mock_download.assert_called_once_with(['mock_link'], None, 'requests')
        mock_make_dataframe.assert_called_once()
        self.assertIsInstance(result, DataFrame)


if __name__ == '__main__':
    unittest.main()