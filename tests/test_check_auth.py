"""
@Author: Bianca Popu (bia1708)
@Date: 25/05/2024
@Links: https://github.com/bia1708/cimple.git
"""
import unittest
from unittest.mock import patch, MagicMock
import subprocess

class TestBashScript(unittest.TestCase):
    @patch('subprocess.run')
    def test_successful_authentication(self, mock_run):
        # Mock the subprocess.run return value for successful authentication
        mock_run.return_value = MagicMock(returncode=0, stdout='User logged in as: correct_user', stderr='')

        git_token = "valid_token"
        username = "correct_user"
        command = ["bash", "path/to/your_script.sh", git_token, username]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertIn('User logged in as', result.stdout)

    @patch('subprocess.run')
    def test_authentication_error(self, mock_run):
        # Mock the subprocess.run return value for authentication error
        mock_run.return_value = MagicMock(returncode=1, stdout='', stderr='Authentication error. Please check your git credentials and try again.')

        git_token = "invalid_token"
        username = "correct_user"
        command = ["bash", "path/to/your_script.sh", git_token, username]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        self.assertEqual(result.returncode, 1)
        self.assertIn('Authentication error', result.stderr)

    @patch('subprocess.run')
    def test_username_token_mismatch(self, mock_run):
        # Mock the subprocess.run return value for username and token mismatch
        mock_run.return_value = MagicMock(returncode=2, stdout='', stderr='Username and token don\'t match!')

        git_token = "valid_token"
        username = "incorrect_user"
        command = ["bash", "path/to/your_script.sh", git_token, username]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        self.assertEqual(result.returncode, 2)
        self.assertIn('Username and token don\'t match', result.stderr)

if __name__ == '__main__':
    unittest.main()
