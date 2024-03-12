import pickle

class Server:
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
        return self.j__nlp_file

    def set_url(self, url):
        self.__url = url

    def set_token(self, token):
        self.__token = token

    def set_username(self, username):
        self.__username = username
        
    def set_jnlp_file(self, jnlp_file):
        self.__jnlp_file = jnlp_file
        
    def serialize(self):
        return pickle.dumps(self)
    
    def __str__(self):
        return self.__url + ", " + self.__username + ", " + self.__token + ", " + self.__jnlp_file
