import requests
import os
import subprocess
from domain.server import Server
from repository.persistent_repository import PersistentRepository
from PySide6.QtCore import QObject, Signal


class Configurator(QObject):
    def __init__(self):
        super().__init__()
        self.__instances = PersistentRepository("../artifacts/data.bin")
        self.__current_server = self.__instances.get_current()

    def connect_to_existing_jenkins(self, username, password, jenkins_url):
        for instance in self.__instances.get_all():
            if instance.get_url() == jenkins_url:
                self.__current_server = instance
                self.__instances.update_current(instance)
                return
        pat = self.get_pat(username, password, jenkins_url)
        jnlp_file = self.get_jnlp(username, password, jenkins_url)
        # print("JNLP FILE: " + jnlp_file)
        self.add_jenkins_instance(jenkins_url, username, pat, jnlp_file)

    install_signal = Signal(int, str)

    def perform_fresh_install(self, username, password, proxy):
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
            token = self.get_pat(username, password, "http://localhost:8080")
            self.install_signal.emit(25, "Generated personal access token\nInstalling plugins...\n")
            self.add_jenkins_instance("http://localhost:8080", username, token, "../artifacts/jenkins-cli.jar")
            self.install_plugins()
            self.install_signal.emit(90, "Installed plugins successfully\nConfiguring setup...\n")
            self.disable_security(username, token, "http://localhost:8080")
            self.install_signal.emit(100, "Setup complete\n")
            if proxy is True:
                self.enable_proxy()
        else:
            self.install_signal.emit(-1, "Failed to install Jenkins")

    def install_plugins(self):
        script_path = "./scripts/server_configuration/install_plugins.sh"

        try:
            command = ["/usr/bin/sudo", script_path, self.__current_server.get_username(), self.__current_server.get_token(), self.__current_server.get_jnlp_file(), self.__current_server.get_url()]
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

    def disable_security(self, username, token, url):
        script_path = "./scripts/server_configuration/disable_security.sh"

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
        script_path = "./scripts/server_configuration/enable_proxy.sh"
        self.install_signal.emit(0, "Setting up proxy...\n")

        try:
            command = ["/usr/bin/sudo", script_path]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
            else:
                self.install_signal.emit(100, "Proxy setup complete")
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Proxy setup failed")
            return None, e.returncode

    def get_pat(self, username, password, url):
        script_path = "./scripts/server_configuration/generate_pat.sh"

        try:
            command = ["bash", script_path, username, password, url]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            token = output.split(":")[1]
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
            return token
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Failed to generate personal access token")
            return None, e.returncode

    def get_jnlp(self, username, password, url):
        script_path = "./scripts/server_configuration/get_jar.sh"

        try:
            command = ["bash", script_path, username, password, url]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            jnlp_file = output.split(":")[1]
            exit_code = result.returncode
            if exit_code != 0:
                self.install_signal.emit(-1, "Failed to install Jenkins")
            return jnlp_file
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            self.install_signal.emit(-1, "Failed to get Jenkins jar")
            return None, e.returncode

    def add_jenkins_instance(self, url, username, token, jnlp_file):
        new_server = Server(url, username, token, jnlp_file)
        self.__instances.add(new_server)
        self.__current_server = new_server
        self.__instances.update_current(self.__current_server)

    def load_jobs(self):
        jobs_with_info = []
        jenkins = self.__current_server.to_api_object()
        jobs = jenkins.get_jobs()
        for job in jobs:
            job_name = job['name']
            try:
                last_build_number = jenkins.get_job_info(job_name)['lastCompletedBuild']['number']
            except:
                last_build_number = "N/A"
            try:
                job_result = jenkins.get_build_info(job_name, last_build_number)['result']
            except:
                job_result = "N/A"

            for prop in jenkins.get_job_info(job_name)['property']:
                if "PipelineTriggers" in prop['_class']:
                    github_enabled = "ENABLED"
                else:
                    github_enabled = "DISABLED"
            jobs_with_info.append([job_name, last_build_number.__str__(), job_result, github_enabled])

        return jobs_with_info

    def set_current_server(self, url):
        for server in self.__instances.get_all():
            if server.get_url() == url:
                self.__current_server = server
                self.__instances.update_current(server)
                break

    def get_current_server(self):
        return self.__current_server

    def get_all_servers(self):
        return self.__instances.get_all()

    def get_number_of_servers(self):
        return len(self.__instances.get_all())

    def close(self):
        self.__instances.close()
