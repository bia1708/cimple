import requests
import os

class Configurator:
    def __init__(self, jenkins_url, api_token):
        self.jenkins_url = ""
        self.api_token = ""

    def connect_to_existing_jenkins(self):
        # Implement logic to connect to an existing Jenkins instance
        # This could involve obtaining user input for Jenkins URL, credentials, etc.
        pass

    def perform_fresh_install(self):
        # Implement logic for performing a fresh Jenkins install
        # This might involve downloading and installing Jenkins, configuring initial settings, etc.
        script_path = 'scripts/fresh_install.sh'
        output = os.popen('bash ' + script_path).read()
        print(output)
