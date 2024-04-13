import unittest
import os
from tempfile import NamedTemporaryFile
from src.repository.persistent_repository import PersistentRepository

class TestPersistentRepository(unittest.TestCase):
    def setUp(self):
        self.tempfile = NamedTemporaryFile(delete=False)
        self.filename = self.tempfile.name
        self.repo = PersistentRepository(self.filename)

    def tearDown(self):
        self.tempfile.close()
        os.unlink(self.filename)

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

    def test_get_current(self):
        self.assertIsNone(self.repo.get_current())
        self.repo.add("item1")
        self.assertEqual(self.repo.get_current(), "item1")
