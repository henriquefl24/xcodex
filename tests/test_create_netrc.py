import unittest
from unittest.mock import patch, mock_open
from xcodex.Util.create_netrc import create_netrc
import os


class TestCreateNetrc(unittest.TestCase):
    @patch('xcodex.Util.create_netrc.expanduser', return_value='/mock/home')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_netrc(self, mock_open, mock_expanduser):
        username = 'test_user'
        password = 'test_pass'
        create_netrc(username, password)

        # Check if expanduser was called correctly
        mock_expanduser.assert_called_once_with("~")

        # Check if open was called with the correct path and mode
        expected_path = os.path.join('/mock/home', '.netrc')
        mock_open.assert_called_once_with(expected_path, 'w')

        # Check if the correct content was written to the file
        mock_open().write.assert_called_once_with(f"machine urs.earthdata.nasa.gov login {username} password {password}\n")


if __name__ == '__main__':
    unittest.main()