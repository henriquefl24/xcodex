import unittest
from unittest.mock import patch, mock_open
from xcodex.Util.create_dodsrc import create_dodsrc
import os


class TestCreateDodsrc(unittest.TestCase):
    @patch('xcodex.Util.create_dodsrc.expanduser', return_value='/mock/home')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_dodsrc(self, mock_open, mock_expanduser):
        create_dodsrc()

        # Check if expanduser was called correctly
        mock_expanduser.assert_called_once_with("~")

        # Check if open was called with the correct path and mode
        expected_path = os.path.join('/mock/home', '.dodsrc')
        mock_open.assert_called_once_with(expected_path, 'w')

        # Check if the correct content was written to the file
        mock_open().write.assert_any_call("HTTP.COOKIEJAR = ~/.urs_cookies\n")
        mock_open().write.assert_any_call("HTTP.NETRC = ~/.netrc\n")


if __name__ == '__main__':
    unittest.main()