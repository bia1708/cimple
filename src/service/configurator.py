"""
@Author: Bianca Popu (bia1708)
@Date: 8/03/2024
@Links: https://github.com/bia1708/cimple.git
"""
import subprocess
from PySide6.QtCore import QObject, Signal

from src.domain.server import Server
from src.repository.persistent_repository import PersistentRepository


class Configurator(QObject):
    """
    Configurator class for servers. Contains all server-interaction utilities.
    Can only be initialized once.
    :ivar initialized: `boolean` indicating whether the class is initialized
    :ivar __instances: `PersistentRepository` repository to hold added servers
    :ivar __current_server: `Server` instance to hold current server
    :ivar connect_signal: `Signal` signal used to update "Connect to Server" View
    :ivar install_signal: `Signal` signal used to update "Install Server" View
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the singleton instance
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # To avoid re-initialization
            super().__init__()
            self.initialized = True
            self.__instances = PersistentRepository("./artifacts/data.bin")
            self.__current_server = self.__instances.get_current()

    connect_signal = Signal(int, str)

    def connect_to_existing_jenkins(self, username, password, jenkins_url, plugins):
        """
        Function which connects to a Jenkins server and adds it to the repository.
        :param username: `str` Jenkins username
        :param password: `str` Jenkins password
        :param jenkins_url: `str` Jenkins url
        :param plugins: `boolean` indicating whether plugins should be installed
        """
        # Check whether the server exists in the repository already and emit signal if so.
        for instance in self.__instances.get_all():
            if instance.get_url() == jenkins_url:
                self.__current_server = instance
                self.__instances.update_current(instance)
                self.connect_signal.emit(-1, "Server already exists!")
                return

        # Get API Token for the given server and user
        token = self.get_token(username, password, jenkins_url)
        if token is not None:
            # Get jnlp file from the new server
            jnlp_file = self.get_jnlp(username, password, jenkins_url)
            if jnlp_file is not None:
                # Add user's jenkins credentials to the remote jenkins server
                self.add_jenkins_credentials(username, token, jnlp_file, jenkins_url)
                # Add new server to the repository
                self.add_jenkins_instance(jenkins_url, username, token, jnlp_file)
                if plugins is True:
                    # If the user checked the plugin installation, do that
                    self.install_plugins(username, token, jnlp_file, jenkins_url)
                # Emit success signal
                self.connect_signal.emit(1, "Successfully connected to server!")

    install_signal = Signal(int, str)

    def perform_fresh_install(self, username, password, proxy):
        """
        Function which performs fresh installation and configuration of Jenkins. Requires sudo privileges.
        Signals are emitted at various steps during installation in order to update the UI (progress bar).
        :param username: `str` Jenkins username
        :param password: `str` Jenkins password
        :param proxy: `boolean` indicating whether proxy should be enabled
        """
        script_path = "./scripts/server_configuration/fresh_install.sh"

        try:
            self.install_signal.emit(0, "Installing Jenkins...\n")
            command = ["/usr/bin/sudo", script_path, username, password]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
            output = result.stdout.strip()
            exit_code = result.returncode

            print(output, exit_code)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode
        if exit_code == 0:
            self.install_signal.emit(20, "Installed Jenkins successfully\nGenerating personal access token...\n")
            token = self.get_token(username, password, "http://localhost:8080")
            self.install_signal.emit(25, "Generated personal access token\nInstalling plugins...\n")
            self.add_jenkins_instance("http://localhost:8080", username, token, "./artifacts/jenkins-cli.jar")
            self.install_plugins(username, token, "./artifacts/jenkins-cli.jar", "http://localhost:8080")
            self.install_signal.emit(90, "Installed plugins successfully\nConfiguring setup...\n")
            self.config_setup(username, token, "http://localhost:8080")
            self.add_jenkins_credentials(username, token, "./artifacts/jenkins-cli.jar", "http://localhost:8080")
            self.install_signal.emit(100, "Setup complete\n")
            if proxy is True:
                self.enable_proxy()
        else:
            self.install_signal.emit(-1, "Failed to install Jenkins")

    def install_plugins(self, username, token, jnlp, url):
        """
        Function which installs cimple plugins to the given Jenkins server.
        :param username: `str` Jenkins username
        :param token: `str` Jenkins token
        :param jnlp: `str` Jenkins CLI file
        :param url: `str` Jenkins URL
        """
        script_path = "./scripts/server_configuration/install_plugins.sh"

        try:
            command = ["bash", script_path, username, token, jnlp, url]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Failed to install plugins")
            return None, e.returncode

    def config_setup(self, username, token, url):
        """
        Function which configures the Jenkins server. Requires sudo privileges.
        :param username: `str` Jenkins username
        :param token: `str` Jenkins token
        :param url: `str` Jenkins URL
        """
        script_path = "./scripts/server_configuration/setup_config.sh"

        try:
            command = ["/usr/bin/sudo", script_path, username, token, url]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Failed to configure Jenkins")
            return None, e.returncode

    def enable_proxy(self):
        """
        Function which enables reverse-proxy (web tunneling) through smee. Requires sudo privileges.
        """
        script_path = "./scripts/server_configuration/enable_proxy.sh"
        self.install_signal.emit(0, "Setting up proxy...\n")

        try:
            command = ["/usr/bin/sudo", script_path]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            print(output)
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
                return -1
            else:
                self.install_signal.emit(100, "Proxy setup complete")
                return 0
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Proxy setup failed")
            return None, e.returncode

    def get_token(self, username, password, url):
        """
        Function which retrieves the Jenkins API token of the user.
        :param username: `str` Jenkins username
        :param password: `str` Jenkins password
        :param url: `str` Jenkins URL
        :return: `str` Jenkins API token
        """
        script_path = "./scripts/server_configuration/generate_pat.sh"

        try:
            command = ["bash", script_path, username, password, url]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            print(output)
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
                self.connect_signal.emit(-1, "Failed to authenticate you!")
                return None
            else:
                # Token is printed to the console in the Bash helper script with the pattern "token:<token>"
                token = output.split(":")[1]
                return token
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Failed to generate personal access token")
            return None, e.returncode

    def get_jnlp(self, username, password, url):
        """
        Function which retrieves the Jenkins CLI file.
        :param username: `str` Jenkins username
        :param password: `str` Jenkins password
        :param url: `str` Jenkins URL
        :return: `str` Jenkins CLI file path
        """
        script_path = "./scripts/server_configuration/get_jar.sh"

        try:
            command = ["bash", script_path, username, password, url]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            print(output)
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
                self.connect_signal.emit(-1, "Failed to authenticate you!")
                return None
            else:
                # JNLP file is printed to the console in the Bash helper script with the pattern "jnlp:<jnlp_file>"
                jnlp_file = output.split(":")[1]
                return jnlp_file
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Failed to get Jenkins jar")
            return None, e.returncode

    def add_jenkins_credentials(self, username, token, jnlp, url):
        """
        Function which adds the Jenkins credentials to the Jenkins server. This is needed when the user enables
        GitHub Integration for a job, for wget-ting the console output of the current job.
        :param username: `str` Jenkins username
        :param token: `str` Jenkins token
        :param jnlp: `str` Jenkins Jar file path
        :param url: `str` Jenkins URL
        """
        script_path = "./scripts/server_configuration/add_jenkins_credentials.sh"

        try:
            command = ["bash", script_path, username, token, jnlp, url]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode

    def add_jenkins_instance(self, url, username, token, jnlp_file):
        """
        Function which adds a Jenkins server to the repository and updates the current Jenkins instance.
        :param url: `str` Jenkins URL
        :param username: `str` Jenkins username
        :param token: `str` Jenkins token
        :param jnlp_file: `str` Jenkins Jar file path
        """
        new_server = Server(url, username, token, jnlp_file)
        self.__instances.add(new_server)
        self.__current_server = new_server
        self.__instances.update_current(self.__current_server)

    def load_jobs(self):
        """
        Function which retrieves all the jobs of the current Jenkins server. Each job is represented as a list, containing:
            - `str` job_name
            - `str` build_number
            - `str` job_result
            - `bool` github_enabled
            - `str` last_build_url
            - `str` artifacts_url
        :return: `List<List>` List of all jobs. Each job is a list.
        """
        jobs_with_info = []
        jenkins = self.__current_server.to_api_object()
        jobs = jenkins.get_jobs()
        for job in jobs:
            job_name = job['name']
            job_info = None
            build_info = None
            last_build_url = None
            artifacts_url = None
            current_build_number = "N/A"

            try:
                job_info = jenkins.get_job_info(job_name)
            except:
                pass

            try:
                last_build_url = job_info['lastBuild']['url']
            except:
                pass

            try:
                current_build_number = job_info['builds'][0]['number']
            except:
                pass

            try:
                artifacts_url = job_info['lastSuccessfulBuild']['url']
            except:
                pass

            try:
                build_info = jenkins.get_build_info(job_name, current_build_number)
                running = build_info['building']
                if running is True:
                    job_result = "RUNNING"
                else:
                    job_result = build_info['result']
            except:
                job_result = "N/A"

            github_enabled = "DISABLED"
            try:
                if "property" in job_info.keys():
                    for prop in job_info['property']:
                        if "PipelineTriggers" in prop['_class']:
                            github_enabled = "ENABLED"
            except:
                pass
            jobs_with_info.append([job_name, current_build_number.__str__(), job_result, github_enabled, last_build_url, artifacts_url])

        return jobs_with_info

    def set_current_server(self, url):
        """
        Function which sets the current server to the one given by the URL.
        :param url: `str` Jenkins URL
        """
        for server in self.__instances.get_all():
            if server.get_url() == url:
                self.__current_server = server
                self.__instances.update_current(server)
                break

    def get_current_server(self):
        """
        Function which returns the current server.
        :return: `Server` object of the current server.
        """
        return self.__current_server

    def get_all_servers(self):
        """
        Function which retrieves all servers.
        :return: `List` List of all servers.
        """
        return self.__instances.get_all()

    def get_number_of_servers(self):
        """
        Function which returns the number of servers.
        :return: `int` Number of servers.
        """
        return len(self.__instances.get_all())

    def get_server_by_url(self, url):
        """
        Function which retrieves the server with the given url.
        :param url: `str` Jenkins URL
        :return: `Server` object of the server with the given url.
        """
        return self.__instances.get_server_by_url(url)

    def close(self):
        """
        Function which closes the repository (writes data to file before exiting).
        """
        self.__instances.close()

    def remove(self, server):
        """
        Function which removes the server given by URL from the repository.
        :param server: `str` Jenkins URL
        """
        self.__instances.delete(self.__instances.get_server_by_url(server))
