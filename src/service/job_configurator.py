"""
@Author: Bianca Popu (bia1708)
@Date: 17/03/2024
@Links: https://github.com/bia1708/cimple.git
"""
import subprocess
from PySide6.QtCore import QObject, Signal

from src.domain.git_repo import GitRepo
from src.domain.job import *


class JobConfigurator(QObject):
    """
    Configurator Class for job configuration. Contains all the methods needed to configure jobs.
    :ivar __server: `Server` current server instance
    """
    def __init__(self, server):
        super().__init__()
        self.__server = server

    def create_job(self, git_repo, git_status):
        """
        Function to create a new job
        :param git_repo: `GitRepo` repository instance
        :param git_status: `boolean` indicating whether the user has enabled GitHub Integration
        """
        # Get the job type needed by checking the repository language
        job_type = self.get_repo_language(git_repo)
        print("Job type: " + job_type)

        # Create .ini file used by jenkins-job-builder
        self.create_jenkins_jobs_ini()

        # Create job by using the JobFactory. jenkinsfile will be initializes based on job_type
        new_job = JobFactory.create_job(job_type, git_repo, git_status)

        # Get the contents of the correct pipeline script to be used
        jenkinsfile = new_job.get_jenkinsfile()
        pipeline_script_file = open(jenkinsfile, "r")
        pipeline_script = pipeline_script_file.read()
        pipeline_script_file.close()

        # Create "seeder.yml" file and load into it the seeder_template with the correct pipeline script
        with open("scripts/job_configuration/seeder_template.yml") as seeder_template_file:
            seeder_script = seeder_template_file.read()
        seeder_template_file.close()
        seeder_script = f"{seeder_script}".replace("{script}", pipeline_script)
        seeder_script_file = open("scripts/job_configuration/seeder.yml", "w")
        seeder_script_file.write(seeder_script)
        seeder_script_file.close()

        script_path = "scripts/job_configuration/create_job.sh"
        try:
            command = ["bash", script_path, git_repo.get_repo_name(), self.__server.get_jnlp_file(),
                       self.__server.get_url(), self.__server.get_username(), self.__server.get_token()]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def init_repo(self, repo_name, git_username, git_pat, git_status):
        """
        Function which initializes a repository job.
        :param repo_name: `str` name of the repository
        :param git_username: `str` git username
        :param git_pat: `str` git PAT
        :param git_status: `boolean` indicating whether the user has enabled GitHub Integration
        """
        git_repo = GitRepo(repo_name, git_username, git_pat)
        self.init_gh(git_pat, git_username, repo_name, self.__server.get_username(), self.__server.get_token(),
                     self.__server.get_jnlp_file(), self.__server.get_url())
        if git_status is True:
            self.setup_webhooks(git_repo)
        self.create_job(git_repo, git_status)

    def init_gh(self, git_pat, git_username, repo_name, username, token, jnlp, url):
        """
        Function which authenticates the user to GitHub CLI (gh)
        :param git_pat: `str` git PAT
        :param git_username: `str` git username
        :param repo_name: `str` name of the repository
        :param username: `str` Jenkins server username
        :param token: `str` Jenkins server token
        :param jnlp: `str` Jenkins server JNLP file path
        :param url: `str` Jenkins server url
        """
        script_path = "./scripts/job_configuration/git_auth.sh"

        try:
            command = ["bash", script_path, git_pat, git_username, repo_name, username, token, jnlp, url]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def setup_webhooks(self, git_repo):
        """
        Function which enables webhooks for the given repository.
        :param git_repo: `GitRepo` repository instance
        """
        script_path = "./scripts/job_configuration/enable_webhooks.sh"

        try:
            command = ["bash", script_path, git_repo.get_repo_name(), git_repo.get_git_username(),
                       git_repo.get_git_pat(), self.__server.get_token(), self.__server.get_username(),
                       self.__server.get_url(), self.__server.get_jnlp_file()]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def get_repo_language(self, git_repo):
        """
        Function which gets the language of the repository.
        :param git_repo: `GitRepo` repository instance
        :return: `str` language of the repository
        """
        script_path = "./scripts/job_configuration/get_repo_language.sh"

        try:
            command = ["bash", script_path, git_repo.get_repo_name()]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            exit_code = result.returncode
            if exit_code == 0:
                language = output.split(":")[1].replace("\"", "")
                return language
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def create_jenkins_jobs_ini(self):
        """
        Function which creates the .ini file for jenkins-job-builder, using current server data:
            - `str` username
            - `str` token
            - `str` URL
        """
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

        ini_file = open("artifacts/jenkins_jobs.ini", "w")
        ini_file.write(text)
        ini_file.close()

    def run_job(self, job):
        """
        Function which triggers a pipeline run by the given job name.
        :param job: `str` job name
        """
        script_path = "./scripts/job_configuration/run_job.sh"

        try:
            command = ["bash", script_path, self.__server.get_jnlp_file(), self.__server.get_username(),
                       self.__server.get_token(), self.__server.get_url(), job]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    auth_signal = Signal(int, str)

    def validate_gh_credentials(self, git_pat, git_username):
        """
        Function which validates the user's git credentials (tries authentication, validates that the token belongs to
        the user). Signals are sent to the UI in order to update it accordingly.
        :param git_pat: `str` GitHub PAT
        :param git_username: `str` git username
        """
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
        """
        Function which validates the given token's permissions (needed permissions are: gist, repo:hook).
        Signals are sent to the UI in order to update it accordingly.
        :param git_pat: `str` GitHub PAT
        """
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
        """
        Function which validates that the given repository exists.
        Signals are sent to the UI in order to update it accordingly.
        :param username: `str` username
        :param git_repo: `str` repository link
        :return:
        """
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
