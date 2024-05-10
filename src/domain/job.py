
class Job:
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
    def __init__(self, git_repo, git_status):
        if git_status is True:
            jenkinsfile = "./scripts/job_configuration/generate_job_python_with_git.groovy"
        else:
            jenkinsfile = "./scripts/job_configuration/generate_job_python.groovy"
        super().__init__(jenkinsfile, git_repo, git_status)


class CppJob(Job):
    def __init__(self, git_repo, git_status):
        if git_status is True:
            jenkinsfile = "./scripts/job_configuration/generate_job_cpp_with_git.groovy"
        else:
            jenkinsfile = "./scripts/job_configuration/generate_job_cpp.groovy"
        super().__init__(jenkinsfile, git_repo, git_status)


class JobFactory:
    @staticmethod
    def create_job(job_type, git_repo, git_status):
        if job_type == "Python":
            return PythonJob(git_repo, git_status)
        elif job_type == "C++":
            return CppJob(git_repo, git_status)
        else:
            raise ValueError("Unknown job type")