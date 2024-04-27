import subprocess
import os
from repository.repository import Repository
from domain.git_repo import Git_Repo

class JobConfigurator:
    def __init__(self, server):
        self.__server = server
        # self.__jobs = Repository()

    def create_job(self, git_repo):
        # os.mkdir(f"../artifacts/{git_repo.get_repo_name()}")
        self.parse_repo(git_repo)
        self.create_jenkins_jobs_ini()

        script_path = "./scripts/job_configuration/create_job.sh"
        try:
            command = ["/bin/sudo", script_path, git_repo.get_repo_name(), self.__server.get_jnlp_file(), self.__server.get_url(), self.__server.get_username(), self.__server.get_token()]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def init_repo(self, repo_name, git_username, git_pat):
        git_repo = Git_Repo(repo_name, git_username, git_pat)
        self.init_gh(git_pat, git_username, repo_name, self.__server.get_username(), self.__server.get_token())
        # self.setup_webhooks(git_repo)
        job = self.create_job(git_repo)
        # self.__jobs.add(job)

    def init_gh(self, git_pat, git_username, repo_name, username, pat):
        # TODO: MAKE SURE YOU ASK FOR GIST ACCESS: https://cli.github.com/manual/gh_auth_login
        # TODO: maybe validate username+token based on gh auth status output
        script_path = "./scripts/job_configuration/git_auth.sh"

        try:
            command = ["bash", script_path, git_pat, git_username, repo_name, username, pat]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def setup_webhooks(self, git_repo):
        script_path = "./scripts/job_configuration/enable_webhooks.sh"

        try:
            command = ["bash", script_path, git_repo.get_repo_name(), git_repo.get_git_username(), self.__server.get_url()]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

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
        # Create .ini script for Jenkins Job Builder connection
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

    def validate_gh_credentials(self, git_username, git_pat, repo_name, username, token, needs_gist):
        script_path = "./scripts/job_configuration/git_auth.sh"

        try:
            command = ["bash", script_path, git_username, git_pat, repo_name, username, token]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode