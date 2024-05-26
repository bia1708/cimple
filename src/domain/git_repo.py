"""
@Author: Bianca Popu (bia1708)
@Date: 17/03/2024
@Links: https://github.com/bia1708/cimple.git
"""


class GitRepo:
    """
    Domain class for Git Repositories (projects)
    :param repo_name: `str` Name of the repository
    :param git_username: `str` Git username
    :param git_pat: `str` Git Personal Access Token
    :ivar __repo_name: `str` Name of the repository
    :ivar __git_username: `str` Git username
    :ivar __git_pat: `str` Git Personal Access Token
    """
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
