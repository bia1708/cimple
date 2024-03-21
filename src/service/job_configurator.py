import subprocess
import os
from repository.repository import Repository
from domain.git_repo import Git_Repo

class Job_Configurator:
    def __init__(self, server):
        self.__server = server
        self.__jobs = Repository()

    def create_job(self, git_repo):
        # os.mkdir(f"../artifacts/{git_repo.get_repo_name()}")
        # self.parse_repo(git_repo)
        self.create_jenkins_jobs_ini()

        script_path = "./scripts/job_configuration/create_job.sh"
        try:
            command = ["bash", script_path]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def init_repo(self, repo_name, git_username, git_pat):
        git_repo = Git_Repo(repo_name, git_username, git_pat)
        self.init_gh(git_pat)
        job = self.create_job(git_repo)
        # self.__jobs.add(job)

    def init_gh(self, git_pat):
        # TODO: MAKE SURE YOU ASK FOR GIST ACCESS: https://cli.github.com/manual/gh_auth_login
        # TODO: maybe validate username+token based og gh auth status output
        script_path = "./scripts/job_configuration/git_auth.sh"

        try:
            command = ["bash", script_path, git_pat]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def parse_repo(self, git_repo):
        script_path = "./scripts/job_configuration/parse_repo.sh"

        try:
            command = ["bash", script_path, git_repo.get_git_username(), git_repo.get_repo_name()]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            # print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def create_jenkins_jobs_ini(self):
        text = "[job_builder]\n" + \
            "ignore_cache=True\n" + \
            "keep_descriptions=False\n" + \
            "include_path=.\n" + \
            "recursive=False\n" + \
            "allow_duplicates=False\n\n" + \
            "[jenkins]\n" + \
            f"user={self.__server.get_username()}\n" + \
            f"password={self.__server.get_token()}\n" + \
            f"url={self.__server.get_url()}\n"

        ini_file = open("../artifacts/jenkins_jobs.ini", "w")
        ini_file.write(text)
        ini_file.close()