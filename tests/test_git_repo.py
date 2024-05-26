"""
@Author: Bianca Popu (bia1708)
@Date: 25/05/2024
@Links: https://github.com/bia1708/cimple.git
"""
import unittest
from src.domain.git_repo import GitRepo

class TestGitRepo(unittest.TestCase):
    def setUp(self):
        self.repo = GitRepo("sample_repo", "sample_username", "sample_pat")

    def test_getters(self):
        # Test the getters
        self.assertEqual(self.repo.get_repo_name(), "sample_repo")
        self.assertEqual(self.repo.get_git_username(), "sample_username")
        self.assertEqual(self.repo.get_git_pat(), "sample_pat")

    def test_setters(self):
        # Test the setters
        self.repo.set_repo_name("new_repo_name")
        self.assertEqual(self.repo.get_repo_name(), "new_repo_name")

        self.repo.set_git_username("new_username")
        self.assertEqual(self.repo.get_git_username(), "new_username")

        self.repo.set_git_pat("new_pat")
        self.assertEqual(self.repo.get_git_pat(), "new_pat")