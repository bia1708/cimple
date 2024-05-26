"""
@Author: Bianca Popu (bia1708)
@Date: 25/05/2024
@Links: https://github.com/bia1708/cimple.git
"""
import unittest
from src.domain.job import *

class TestJob(unittest.TestCase):
    def setUp(self):
        self.job = Job("jenkinsfile_path", "git_repo_url", True)

    def test_getters(self):
        # Test the getters
        self.assertEqual(self.job.get_jenkinsfile(), "jenkinsfile_path")
        self.assertEqual(self.job.get_git_repo(), "git_repo_url")
        self.assertEqual(self.job.get_git_status(), True)

    def test_setters(self):
        # Test the setters
        self.job.set_jenkinsfile("new_jenkinsfile_path")
        self.assertEqual(self.job.get_jenkinsfile(), "new_jenkinsfile_path")

        self.job.set_git_repo("new_git_repo_url")
        self.assertEqual(self.job.get_git_repo(), "new_git_repo_url")

        self.job.set_git_status(False)
        self.assertEqual(self.job.get_git_status(), False)

class TestPythonJob(unittest.TestCase):
    def test_initialization(self):
        job = PythonJob("git_repo_url", True)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_python_with_git.groovy")
        self.assertEqual(job.get_git_repo(), "git_repo_url")
        self.assertEqual(job.get_git_status(), True)

        job = PythonJob("git_repo_url", False)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_python.groovy")
        self.assertEqual(job.get_git_repo(), "git_repo_url")
        self.assertEqual(job.get_git_status(), False)

class TestCppJob(unittest.TestCase):
    def test_initialization(self):
        job = CppJob("git_repo_url", True)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_cpp_with_git.groovy")
        self.assertEqual(job.get_git_repo(), "git_repo_url")
        self.assertEqual(job.get_git_status(), True)

        job = CppJob("git_repo_url", False)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_cpp.groovy")
        self.assertEqual(job.get_git_repo(), "git_repo_url")
        self.assertEqual(job.get_git_status(), False)

class TestJavaJob(unittest.TestCase):
    def test_initialization(self):
        job = JavaJob("git_repo_url", True)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_java_with_git.groovy")
        self.assertEqual(job.get_git_repo(), "git_repo_url")
        self.assertEqual(job.get_git_status(), True)

        job = JavaJob("git_repo_url", False)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_java.groovy")
        self.assertEqual(job.get_git_repo(), "git_repo_url")
        self.assertEqual(job.get_git_status(), False)

class TestJobFactory(unittest.TestCase):
    def test_create_job(self):
        job = JobFactory.create_job("Python", "git_repo_url", True)
        self.assertIsInstance(job, PythonJob)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_python_with_git.groovy")

        job = JobFactory.create_job("C++", "git_repo_url", True)
        self.assertIsInstance(job, CppJob)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_cpp_with_git.groovy")

        job = JobFactory.create_job("Java", "git_repo_url", True)
        self.assertIsInstance(job, JavaJob)
        self.assertEqual(job.get_jenkinsfile(), "scripts/job_configuration/generate_job_java_with_git.groovy")

        with self.assertRaises(ValueError):
            JobFactory.create_job("Unknown", "git_repo_url", True)