from repository.repository import Repository

class Job_Configurator:
    def _init__(self, server):
        self.__server = server
        self.__jobs = Repository()
        
    def create_job(self, git_repo, git_username, git_pat):
        pass