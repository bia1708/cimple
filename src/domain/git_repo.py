class Git_Repo:
    def __init__(self, repo_name, git_username, git_pat):
        self.__repo_name = repo_name
        self.__git_username = git_username
        self.__git_pat = git_pat

    def get_repo_name(self):
        return self.__repo_name

    def get_git_username(self):
        return self.__git_username

    def get_git_pat(self):
        return self.__git_pat

    def set_repo_name(self, repo_name):
        self.__repo_name = repo_name

    def set_git_username(self, git_username):
        self.__git_username = git_username

    def set_git_pat(self, git_pat):
        self.__git_pat = git_pat