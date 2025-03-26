import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
import requests
import sys
import io
from xcodex.Util.download import download

class TestDownload(unittest.TestCase):

    @patch('xcodex.Util.download.getpass', return_value='password')
    @patch('xcodex.Util.download.input', return_value='username')
    @patch('xcodex.Util.download.requests.head')
    @patch('xcodex.Util.download.requests.Session.get')
    @patch('xcodex.Util.download.exists')
    @patch('xcodex.Util.download.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_download(self, mock_open, mock_makedirs, mock_exists, mock_get, mock_head, mock_input, mock_getpass):
        # Suppress stdout and stderr
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        sys_stderr = sys.stderr
        sys.stdout = captured_output
        sys.stderr = captured_output

        try:
            # Mock responses
            mock_exists.side_effect = [False, False, False]  # For .netrc, .dodsrc, and file_path
            mock_head.return_value.headers = {'content-length': '100'}
            mock_get.return_value.__enter__.return_value.iter_content = lambda chunk_size: [b'0' * 10] * 10
            mock_get.return_value.__enter__.return_value.status_code = 200
            mock_get.return_value.__enter__.return_value.headers = {'content-length': '100'}

            # Call the download function
            download(['http://example.com/file.nc4'])

            # Assertions
            mock_makedirs.assert_called_once_with(os.path.abspath('downloaded_data'), exist_ok=True)
            mock_open.assert_any_call(os.path.abspath(os.path.join('downloaded_data', 'file.nc4')), 'wb')
            self.assertEqual(mock_get.call_count, 1)
        finally:
            # Restore stdout and stderr
            sys.stdout = sys_stdout
            sys.stderr = sys_stderr

    @patch('xcodex.Util.download.getpass', return_value='password')
    @patch('xcodex.Util.download.input', return_value='nickname')
    @patch('xcodex.Util.download.requests.head')
    @patch('xcodex.Util.download.requests.Session.get')
    @patch('xcodex.Util.download.exists')
    @patch('xcodex.Util.download.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_with_retries(self, mock_open, mock_makedirs, mock_exists, mock_get, mock_head, mock_input, mock_getpass):
        # Suppress stdout and stderr
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        sys_stderr = sys.stderr
        sys.stdout = captured_output
        sys.stderr = captured_output

        try:
            # Mock responses
            mock_exists.side_effect = [False, False, False]  # For .netrc, .dodsrc, and file_path
            mock_head.return_value.headers = {'content-length': '100'}
            mock_get.side_effect = [requests.exceptions.RequestException] * 5 + [
                MagicMock(status_code=200, headers={'content-length': '100'},
                          iter_content=lambda chunk_size: [b'0' * 10] * 10)]

            # Call the download function
            download(['https://example.com/file.nc4'])

            # Assertions
            self.assertEqual(mock_get.call_count, 6)
            mock_open.assert_any_call(os.path.abspath(os.path.join('downloaded_data', 'file.nc4')), 'wb')
        finally:
            # Restore stdout and stderr
            sys.stdout = sys_stdout
            sys.stderr = sys_stderr

    @patch('xcodex.Util.download.getpass', return_value='password')
    @patch('xcodex.Util.download.input', return_value='username')
    @patch('xcodex.Util.download.requests.head')
    @patch('xcodex.Util.download.requests.Session.get')
    @patch('xcodex.Util.download.exists')
    @patch('xcodex.Util.download.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_invalid_links(self, mock_open, mock_makedirs, mock_exists, mock_get, mock_head, mock_input, mock_getpass):
        with self.assertRaises(ValueError):
            download('http://example.com/file.nc4')  # Invalid links parameter

    @patch('xcodex.Util.download.getpass', return_value='password')
    @patch('xcodex.Util.download.input', return_value='username')
    @patch('xcodex.Util.download.requests.head')
    @patch('xcodex.Util.download.requests.Session.get')
    @patch('xcodex.Util.download.exists')
    @patch('xcodex.Util.download.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_invalid_downloaded_data_path(self, mock_open, mock_makedirs, mock_exists, mock_get, mock_head, mock_input, mock_getpass):
        with self.assertRaises(ValueError):
            download(['http://example.com/file.nc4'], downloaded_data_path=123)  # Invalid downloaded_data_path parameter

    @patch('xcodex.Util.download.getpass', return_value='password')
    @patch('xcodex.Util.download.input', return_value='username')
    @patch('xcodex.Util.download.requests.head')
    @patch('xcodex.Util.download.requests.Session.get')
    @patch('xcodex.Util.download.exists')
    @patch('xcodex.Util.download.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_invalid_method(self, mock_open, mock_makedirs, mock_exists, mock_get, mock_head, mock_input, mock_getpass):
        with self.assertRaises(ValueError):
            download(['http://example.com/file.nc4'], method="invalid_method")  # Invalid method parameter

if __name__ == '__main__':
    unittest.main()