import unittest
from src.domain.server import Server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server("http://example.com", "user", "token", "jnlp_file")

    def test_getters(self):
        # Test the getters
        self.assertEqual(self.server.get_url(), "http://example.com")
        self.assertEqual(self.server.get_username(), "user")
        self.assertEqual(self.server.get_token(), "token")
        self.assertEqual(self.server.get_jnlp_file(), "jnlp_file")

    def test_setters(self):
        # Test the setters
        self.server.set_url("http://newurl.com")
        self.assertEqual(self.server.get_url(), "http://newurl.com")

        self.server.set_username("newuser")
        self.assertEqual(self.server.get_username(), "newuser")

        self.server.set_token("newtoken")
        self.assertEqual(self.server.get_token(), "newtoken")

        self.server.set_jnlp_file("new_jnlp_file")
        self.assertEqual(self.server.get_jnlp_file(), "new_jnlp_file")
