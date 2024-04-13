import unittest
from src.repository.repository import Repository

class TestRespository(unittest.TestCase):
    def setUp(self):
        self.repo = Repository()

    def test_add(self):
        self.repo.add("item")
        self.assertIn("item", self.repo.get_all())

    def test_delete(self):
        self.repo.add("item")
        self.repo.delete("item")
        self.assertNotIn("item", self.repo.get_all())

    def test_update(self):
        self.repo.add("old_item")
        self.repo.update("old_item", "new_item")
        self.assertNotIn("old_item", self.repo.get_all())
        self.assertIn("new_item", self.repo.get_all())

    def test_get_all(self):
        self.assertEqual(self.repo.get_all(), [])
