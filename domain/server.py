
class Server:
    def __init__(self, url, username, token):
        self.__url = url
        self.__username = username
        self.__token = token

    def get_url(self):
        return self.__url

    def get_token(self):
        return self.__token

    def get_username(self):
        return self.__username

    def set_url(self, url):
        self.__url = url

    def set_token(self, token):
        self.__token = token

    def set_username(self, username):
        self.__username = username
