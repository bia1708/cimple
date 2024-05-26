"""
@Author: Bianca Popu (bia1708)
@Date: 6/03/2024
@Links: https://github.com/bia1708/cimple.git
"""
from jenkins import Jenkins


class Server:
    """
    Domain class for Jenkins servers
    :param url: `str` URL of Jenkins server
    :param username: `str` username for Jenkins server
    :param token: `str` API token for Jenkins server
    :param jnlp_file: `str` path to JNLP file
    :ivar __url: `str` URL of Jenkins server
    :ivar __username: `str` username for Jenkins server
    :ivar __token: `str` API token for Jenkins server
    :ivar __jnlp_file: `str` path to JNLP file
    """
    def __init__(self, url, username, token, jnlp_file):
        self.__url = url
        self.__username = username
        self.__token = token
        self.__jnlp_file = jnlp_file

    def get_url(self):
        return self.__url

    def get_token(self):
        return self.__token

    def get_username(self):
        return self.__username
    
    def get_jnlp_file(self):
        return self.__jnlp_file

    def set_url(self, url):
        self.__url = url

    def set_token(self, token):
        self.__token = token

    def set_username(self, username):
        self.__username = username

    def set_jnlp_file(self, jnlp_file):
        self.__jnlp_file = jnlp_file

    def to_api_object(self):
        """
        Function to create Jenkins API object from jenkins server
        :return: Jenkins API object
        """
        return Jenkins(self.__url, username=self.__username, password=self.__token)

    def __str__(self):
        return self.__url + ", " + self.__username + ", " + self.__token + ", " + self.__jnlp_file
