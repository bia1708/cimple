
class Job:
    def __init__(self, jenkinsfile, git_repo):
        self.__jenkinsfile = jenkinsfile
        self.__git_repo = git_repo

    def get_jenkinsfile(self):
        return self.__jenkinsfile

    def get_git_repo(self):
        return self.__git_repo

    def set_jenkinsfile(self, jenkinsfile):
        self.__jenkinsfile = jenkinsfile

    def set_git_repo(self, git_repo):
        self.__git_repo = git_repo