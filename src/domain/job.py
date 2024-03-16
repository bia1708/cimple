
class Job:
    def __init__(self, jenkinsfile, repository, git_username, git_token):
        self.__jenkinsfile = jenkinsfile
        self.__repository = repository
        self.__git_username = git_username
        self.__git_token = git_token