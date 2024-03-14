import requests
import os
import subprocess
from domain.server import Server
from repository.persistent_repository import PersistentRepository

class Configurator:
    def __init__(self):
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

    def perform_fresh_install(self, username, password):
        script_path = "./scripts/fresh_install.sh"

        try:
            command = ["/usr/bin/sudo", script_path, username, password]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()
            exit_code = result.returncode
            
            print(output, exit_code)
        except subprocess.CalledProcessError as e:
            # Handle errors if the subprocess returns a non-zero exit code
            print(f"Error: {e}")
            return None, e.returncode
        
        if exit_code == 0:
            token = self.get_pat(username, password, "http://localhost:8080")
            self.add_jenkins_instance("http://localhost:8080", username, token, "../artifacts/jenkins-cli.jar")
            print([str(x) for x in self.__instances.get_all()])
            
    def install_plugins(self):
        script_path = "./scripts/install_plugins.sh"
        
        try:
            command = ["bash", script_path, self.__current_server.get_username(), self.__current_server.get_token(), self.__current_server.get_jnlp_file(), self.__current_server.get_url()]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

            output = result.stderr.strip()            
            # token = output.split(":")[1]
            # return token
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode
            
        
    def get_pat(self, username, password, url):
        script_path = "./scripts/generate_pat.sh"
        
        try:
            command = ["bash", script_path, username, password, url]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()            
            token = output.split(":")[1]
            return token
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode
        
    def get_jnlp(self, username, password, url):
        script_path = "./scripts/get_jar.sh"
        
        try:
            command = ["bash", script_path, username, password, url]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()            
            jnlp_file = output.split(":")[1]
            return jnlp_file
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode
            
    def add_jenkins_instance(self, url, username, token, jnlp_file):
        new_server = Server(url, username, token, jnlp_file)
        self.__instances.add(new_server)
        self.__current_server = new_server
        self.__instances.update_current(self.__current_server)
        
    def extract_variables(self, output):
        pass

    def get_current_server(self):
        return self.__current_server
