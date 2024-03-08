import requests
import os
import subprocess
from domain.server import Server
from repository.repository import Repository

class Configurator:
    def __init__(self, instances):
        self.__instances = Repository()

    def connect_to_existing_jenkins(self, jenkins_url, pat):
        # Implement logic to connect to an existing Jenkins instance
        # This could involve obtaining user input for Jenkins URL, credentials, etc.
        pass

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
            token = self.get_pat(username, password)
            self.add_jenkins_instance("http://localhost:8080", username, token, "../artifacts/jenkins-cli.jar")
            print([str(x) for x in self.__instances.get_all()])
            
        
    def get_pat(self, username, password):
        script_path = "./scripts/generate_pat.sh"
        
        try:
            command = ["bash", script_path, username, password]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

            output = result.stdout.strip()            
            token = output.split(":")[1]
            return token
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None, e.returncode
            
    def add_jenkins_instance(self, url, username, token, jnlp_file):
        new_server = Server(url, username, token, jnlp_file)
        self.__instances.add(new_server)
        
    def extract_variables(self, output):
        pass

config = Configurator("")
config.perform_fresh_install("bia", "1234")
