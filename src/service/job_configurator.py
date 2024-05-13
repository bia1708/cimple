import subprocess
import os
from PySide6.QtCore import QObject, Signal
from repository.repository import Repository
from domain.git_repo import Git_Repo
from domain.job import *

class JobConfigurator(QObject):
    def __init__(self, server):
        super().__init__()
        self.__server = server
        # self.__jobs = Repository()

    def create_job(self, git_repo, git_status):
        # os.mkdir(f"../artifacts/{git_repo.get_repo_name()}")
        # self.parse_repo(git_repo)
        job_type = self.get_repo_language(git_repo)
        self.create_jenkins_jobs_ini()

        new_job = JobFactory.create_job(job_type, git_repo, git_status)
        jenkinsfile = new_job.get_jenkinsfile()
        pipeline_script_file = open(jenkinsfile, "r")

        # if git_status is True:
        #     pipeline_script_file = open("./scripts/job_configuration/generate_job_python_with_git.groovy", "r")
        # else:
        #     pipeline_script_file = open("./scripts/job_configuration/generate_job_python.groovy", "r")
        pipeline_script = pipeline_script_file.read()
        pipeline_script_file.close()
        with open("./scripts/job_configuration/seeder_template.yml") as seeder_template_file:
            seeder_script = seeder_template_file.read()
        seeder_template_file.close()
        seeder_script = f"{seeder_script}".replace("{script}", pipeline_script)
        seeder_script_file = open("./scripts/job_configuration/seeder.yml", "w")
        seeder_script_file.write(seeder_script)
        seeder_script_file.close()

        script_path = "./scripts/job_configuration/create_job.sh"
        try:
            command = ["bash", script_path, git_repo.get_repo_name(), self.__server.get_jnlp_file(), self.__server.get_url(), self.__server.get_username(), self.__server.get_token()]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def init_repo(self, repo_name, git_username, git_pat, git_status):
        git_repo = Git_Repo(repo_name, git_username, git_pat)
        self.init_gh(git_pat, git_username, repo_name, self.__server.get_username(), self.__server.get_token())
        if git_status is True:
            self.setup_webhooks(git_repo)
        job = self.create_job(git_repo, git_status)
        # self.__jobs.add(job)

    def init_gh(self, git_pat, git_username, repo_name, username, pat):
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
            command = ["/usr/bin/sudo", script_path, git_repo.get_repo_name(), git_repo.get_git_username(), git_repo.get_git_pat(), self.__server.get_token(), self.__server.get_username(), self.__server.get_url()]
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

    def get_repo_language(self, git_repo):
        script_path = "./scripts/job_configuration/get_repo_language.sh"

        try:
            command = ["bash", script_path, git_repo.get_git_username(), git_repo.get_repo_name()]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            exit_code = result.returncode
            if exit_code == 0:
                language = output.split(":")[1].replace("\"", "")
                return language
            return None
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

    def run_job(self, job):
        script_path = "./scripts/job_configuration/run_job.sh"

        try:
            command = ["bash", script_path, self.__server.get_jnlp_file(), self.__server.get_username(), self.__server.get_token(),
                       self.__server.get_url(), job]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            # print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    auth_signal = Signal(int, str)

    def validate_gh_credentials(self, git_pat, git_username):
        script_path = "./scripts/job_configuration/check_auth.sh"

        try:
            command = ["bash", script_path, git_pat, git_username]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            exit_code = result.returncode
            print(output)
            print(exit_code)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

        if exit_code == 0:
            self.auth_signal.emit(0, "Authentication completed successfully.")
            return True
        elif exit_code == 1:
            self.auth_signal.emit(1, "Authentication error. Please check your git credentials and try again.")
        elif exit_code == 2:
            self.auth_signal.emit(2, "Username and token don't match!")
        return False

    def validate_token_permissions(self, git_pat):
        script_path = "./scripts/job_configuration/check_git_pat_permissions.sh"

        try:
            command = ["bash", script_path, git_pat]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            exit_code = result.returncode
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode
        
        if exit_code == 0:
            self.auth_signal.emit(0, "Token has the required permissions.")
            return True
        elif exit_code == 142:
            self.auth_signal.emit(1, "Your token needs Gist permissions.")
        elif exit_code ==242:
            self.auth_signal.emit(2, "Your token needs repo_hook permissions.")
        return False

    def validate_repo_exists(self, username, git_repo):
        script_path = "./scripts/job_configuration/check_git_repo_exists.sh"

        try:
            command = ["bash", script_path, username, git_repo]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            exit_code = result.returncode
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

        if exit_code == 0:
            self.auth_signal.emit(0, "Repository validated.")
            return True
        elif exit_code == 128:
            self.auth_signal.emit(1, "The provided repository does not exist.")
        elif exit_code ==1:
            self.auth_signal.emit(2, "Repository does not belong to the provided user.")
        return False
