import unittest
from unittest.mock import patch, MagicMock
from src.service.configurator import Configurator

class TestConfigurator(unittest.TestCase):
    @patch('src.repository.persistent_repository.PersistentRepository')
    def setUp(self, MockPersistentRepository):
        self.configurator = Configurator()
        self.mock_repository = MockPersistentRepository.return_value
        self.mock_repository.get_current.return_value = None
        self.mock_emit = MagicMock()
        self.configurator.install_signal.connect(self.mock_emit)

    @patch('subprocess.run')
    def test_perform_fresh_install_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="token:my_token")

        with patch.object(self.configurator, 'get_pat', return_value='my_token'):
            with patch.object(self.configurator, 'add_jenkins_credentials') as mock_add_creds:
                with patch.object(self.configurator, 'add_jenkins_instance') as mock_add_instance:
                    with patch.object(self.configurator, 'install_plugins') as mock_install_plugins:
                        with patch.object(self.configurator, 'disable_security') as mock_disable_security:
                            self.configurator.perform_fresh_install("username", "password", False)

                            self.mock_emit.assert_any_call(0, "Installing Jenkins...\n")
                            self.mock_emit.assert_any_call(20, "Installed Jenkins successfully\nGenerating personal access token...\n")
                            self.mock_emit.assert_any_call(25, "Generated personal access token\nInstalling plugins...\n")
                            self.mock_emit.assert_any_call(90, "Installed plugins successfully\nConfiguring setup...\n")
                            self.mock_emit.assert_any_call(100, "Setup complete\n")
                            mock_add_creds.assert_called()
                            mock_add_instance.assert_called()
                            mock_install_plugins.assert_called()
                            mock_disable_security.assert_called()


    @patch('subprocess.run')
    def test_perform_fresh_install_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="error")

        self.configurator.perform_fresh_install("username", "password", False)
        self.mock_emit.assert_any_call(-1, "Failed to install Jenkins")

    @patch('subprocess.run')
    def test_install_plugins(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        self.configurator.install_plugins("username", "token", "jnlp", "url")
        self.mock_emit.assert_not_called()

    @patch('subprocess.run')
    def test_disable_security(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        self.configurator.disable_security("username", "token", "url")
        self.mock_emit.assert_not_called()

    def test_singleton_behavior(self):
        configurator1 = Configurator()
        configurator2 = Configurator()
        self.assertIs(configurator1, configurator2)
