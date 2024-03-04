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

    def perform_fresh_install(self, username, password):
        script_path = 'scripts/fresh_install.sh'

        try:
            command = ['bash', script_path] + list(username, password)
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            output = result.stdout.strip()
            exit_code = result.returncode

            print(output, exit_code)
            return output, exit_code
        except subprocess.CalledProcessError as e:
            # Handle errors if the subprocess returns a non-zero exit code
            print(f"Error: {e}")
            return None, e.returncode
