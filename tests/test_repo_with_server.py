import unittest
import os
import pickle
from unittest.mock import patch, MagicMock
from jenkins import Jenkins
from src.repository.repository import Repository
from src.domain.server import Server
from src.repository.persistent_repository import PersistentRepository

class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Setup a mock Jenkins server
        self.server = Server(url="http://mockjenkins.com", username="user", token="token123", jnlp_file="path/to/jnlp")

        # Create a temporary file for PersistentRepository
        self.repo_filename = "artifacts/test_repo.pkl"
        self.repository = PersistentRepository(self.repo_filename)

    def tearDown(self):
        # Clean up the repository file
        if os.path.exists(self.repo_filename):
            os.remove(self.repo_filename)

    def test_server_creation_and_api_object(self):
        # Test creating a Jenkins API object from the server
        jenkins_api = self.server.to_api_object()
        self.assertIsInstance(jenkins_api, Jenkins)
        self.assertEqual(jenkins_api.server, "http://mockjenkins.com/")

    def test_repository_add_and_get(self):
        # Test adding a server to the repository and retrieving it
        self.repository.add(self.server)
        retrieved_server = self.repository.get_server_by_url("http://mockjenkins.com")
        self.assertIsNotNone(retrieved_server)
        self.assertEqual(retrieved_server.get_url(), "http://mockjenkins.com")

    def test_repository_persistence(self):
        # Test if the repository persists data correctly
        self.repository.add(self.server)
        self.repository.close()

        # Re-open the repository and check if the data is still there
        new_repository = PersistentRepository(self.repo_filename)
        retrieved_server = new_repository.get_server_by_url("http://mockjenkins.com")
        self.assertIsNotNone(retrieved_server)
        self.assertEqual(retrieved_server.get_url(), "http://mockjenkins.com")

    def test_repository_delete(self):
        # Test deleting a server from the repository
        self.repository.add(self.server)
        self.repository.delete(self.server)
        retrieved_server = self.repository.get_server_by_url("http://mockjenkins.com")
        self.assertIsNone(retrieved_server)

    def test_repository_update(self):
        # Test updating a server in the repository
        self.repository.add(self.server)
        updated_server = Server(url="http://updatedjenkins.com", username="newuser", token="newtoken", jnlp_file="new/path/to/jnlp")
        self.repository.update(self.server, updated_server)
        retrieved_server = self.repository.get_server_by_url("http://updatedjenkins.com")
        self.assertIsNotNone(retrieved_server)
        self.assertEqual(retrieved_server.get_url(), "http://updatedjenkins.com")

    def test_repository_get_current(self):
        # Test retrieving the current item in the repository
        self.repository.add(self.server)
        current_server = self.repository.get_current()
        self.assertEqual(current_server.get_url(), "http://mockjenkins.com")

    def test_repository_update_current(self):
        # Test updating the current item in the repository
        another_server = Server(url="http://anotherjenkins.com", username="anotheruser", token="anothertoken", jnlp_file="another/path/to/jnlp")
        self.repository.add(self.server)
        self.repository.add(another_server)
        self.repository.update_current(another_server)
        current_server = self.repository.get_current()
        self.assertEqual(current_server.get_url(), "http://anotherjenkins.com")
