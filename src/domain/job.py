"""
@Author: Bianca Popu (bia1708)
@Date: 16/03/2024
@Links: https://github.com/bia1708/cimple.git
"""


class Job:
    """
    Template class for Jenkins Jobs
    :param jenkinsfile: `str` Jenkinsfile to be used for job creation
    :param git_repo: `GitRepo` Git repo to create job for
    :param git_status: `boolean` Whether the job has git status enabled
    :ivar __jenkinsfile: `str` Jenkinsfile to be used for job creation
    :ivar __git_repo: `GitRepo` Git repo to create job for
    :ivar __git_status: `boolean` Whether the job has git status enabled
    """
    def __init__(self, jenkinsfile, git_repo, git_status):
        self.__jenkinsfile = jenkinsfile
        self.__git_repo = git_repo
        self.__git_status = git_status

    def get_jenkinsfile(self):
        return self.__jenkinsfile

    def get_git_repo(self):
        return self.__git_repo

    def get_git_status(self):
        return self.__git_status

    def set_jenkinsfile(self, jenkinsfile):
        self.__jenkinsfile = jenkinsfile

    def set_git_repo(self, git_repo):
        self.__git_repo = git_repo

    def set_git_status(self, status):
        self.__git_status = status


class PythonJob(Job):
    """
    Job subclass for Python Jobs. Initializes jenkinsfile with Python groovy pipeline.
    :param git_repo: `GitRepo` Git repo to create job for
    :param git_status: `boolean` Whether the job has git status enabled
    """
    def __init__(self, git_repo, git_status):
        if git_status is True:
            jenkinsfile = "scripts/job_configuration/generate_job_python_with_git.groovy"
        else:
            jenkinsfile = "scripts/job_configuration/generate_job_python.groovy"
        super().__init__(jenkinsfile, git_repo, git_status)


class CppJob(Job):
    """
    Job subclass for C++ Jobs. Initializes jenkinsfile with C++ groovy pipeline.
    :param git_repo: `GitRepo` Git repo to create job for
    :param git_status: `boolean` Whether the job has git status enabled
    """
    def __init__(self, git_repo, git_status):
        if git_status is True:
            jenkinsfile = "scripts/job_configuration/generate_job_cpp_with_git.groovy"
        else:
            jenkinsfile = "scripts/job_configuration/generate_job_cpp.groovy"
        super().__init__(jenkinsfile, git_repo, git_status)


class JavaJob(Job):
    """
    Job subclass for Java Jobs. Initializes jenkinsfile with Java groovy pipeline.
    :param git_repo: `GitRepo` Git repo to create job for
    :param git_status: `boolean` Whether the job has git status enabled
    """
    def __init__(self, git_repo, git_status):
        if git_status is True:
            jenkinsfile = "scripts/job_configuration/generate_job_java_with_git.groovy"
        else:
            jenkinsfile = "scripts/job_configuration/generate_job_java.groovy"
        super().__init__(jenkinsfile, git_repo, git_status)


class JobFactory:
    """
    Factory class for Jobs
    """
    @staticmethod
    def create_job(job_type, git_repo, git_status):
        """
        Factory method to create Job
        :param job_type: `str` Type of Job (one of 'Python', 'C++', 'Java')
        :param git_repo: `str` Git repo to create job for
        :param git_status: `boolean` Whether the job has git status enabled
        :return: `Job` Job object (one of `PythonJob`, `CppJob`, `JavaJob`)
        """
        if job_type == "Python":
            return PythonJob(git_repo, git_status)
        elif job_type == "C++":
            return CppJob(git_repo, git_status)
        elif job_type == "Java":
            return JavaJob(git_repo, git_status)
        else:
            raise ValueError("Unknown job type")