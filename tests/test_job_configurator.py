"""
@Author: Bianca Popu (bia1708)
@Date: 25/05/2024
@Links: https://github.com/bia1708/cimple.git
"""
import unittest
from unittest.mock import patch, MagicMock, mock_open
from PySide6.QtCore import QObject, Signal
from src.service.job_configurator import JobConfigurator  # Adjust the import path as necessary
from src.domain.server import Server
from src.domain.git_repo import GitRepo

class TestJobConfigurator(unittest.TestCase):
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open, read_data="pipeline_script")
    def setUp(self, mock_file, mock_run):
        self.mock_server = MagicMock(spec=Server)
        self.mock_server.get_jnlp_file.return_value = "mock_jnlp"
        self.mock_server.get_url.return_value = "http://mock_url"
        self.mock_server.get_username.return_value = "mock_user"
        self.mock_server.get_token.return_value = "mock_token"
        self.configurator = JobConfigurator(self.mock_server)
        self.mock_emit = MagicMock()
        self.configurator.auth_signal.connect(self.mock_emit)

    @patch('subprocess.run')
    def test_create_job(self, mock_run):
        mock_git_repo = MagicMock(spec=GitRepo)
        mock_git_repo.get_repo_name.return_value = "mock_repo"
        mock_git_repo.get_git_username.return_value = "mock_git_user"
        mock_git_repo.get_git_pat.return_value = "mock_git_pat"
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        with patch.object(self.configurator, 'get_repo_language', return_value='Python'):
            self.configurator.create_job(mock_git_repo, True)
            mock_run.assert_called()
            self.assertTrue(mock_run.called)

    @patch('subprocess.run')
    def test_init_repo(self, mock_run):
        mock_git_repo = MagicMock(spec=GitRepo)
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        with patch.object(self.configurator, 'get_repo_language', return_value='Python'):
            with patch.object(self.configurator, 'setup_webhooks') as mock_setup_webhooks:
                with patch.object(self.configurator, 'create_job') as mock_create_job:
                    self.configurator.init_repo("repo_name", "git_user", "git_pat", True)
                    mock_setup_webhooks.assert_called()
                    mock_create_job.assert_called()

    @patch('subprocess.run')
    def test_init_gh(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        self.configurator.init_gh("git_pat", "git_user", "repo_name", "user", "token", "jnlp", "url")
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_setup_webhooks(self, mock_run):
        mock_git_repo = MagicMock(spec=GitRepo)
        mock_git_repo.get_repo_name.return_value = "mock_repo"
        mock_git_repo.get_git_username.return_value = "mock_git_user"
        mock_git_repo.get_git_pat.return_value = "mock_git_pat"
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        self.configurator.setup_webhooks(mock_git_repo)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_validate_gh_credentials(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        self.assertTrue(self.configurator.validate_gh_credentials("git_pat", "git_user"))
        self.mock_emit.assert_called_with(0, "Authentication completed successfully.")

        mock_run.return_value = MagicMock(returncode=1, stderr="")
        self.assertFalse(self.configurator.validate_gh_credentials("git_pat", "git_user"))
        self.mock_emit.assert_called_with(1, "Authentication error. Please check your git credentials and try again.")

    @patch('subprocess.run')
    def test_validate_token_permissions(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        self.assertTrue(self.configurator.validate_token_permissions("git_pat"))
        self.mock_emit.assert_called_with(0, "Token has the required permissions.")

        mock_run.return_value = MagicMock(returncode=142, stderr="")
        self.assertFalse(self.configurator.validate_token_permissions("git_pat"))
        self.mock_emit.assert_called_with(1, "Your token needs Gist permissions.")

    @patch('subprocess.run')
    def test_validate_repo_exists(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        self.assertTrue(self.configurator.validate_repo_exists("user", "repo"))
        self.mock_emit.assert_called_with(0, "Repository validated.")

        mock_run.return_value = MagicMock(returncode=128, stderr="")
        self.assertFalse(self.configurator.validate_repo_exists("user", "repo"))
        self.mock_emit.assert_called_with(1, "The provided repository does not exist.")
