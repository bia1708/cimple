from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

if __name__ == '__main__':
    # config = Configurator()
    # config.perform_fresh_install("bia", "1234")
    # config.add_jenkins_instance("mock-url", "mock-username", "mock-token", "mock-jnlp")
    # config.connect_to_existing_jenkins("bia", "1234", "http://localhost:8080")
    # print(config.get_current_server())
    # config.disable_security("bia", "119b79f97505b042d00e578a690af69bd9", "http://localhost:8080")
    # config.install_plugins()
    # config.enable_proxy()
    # job_config = Job_Configurator(config.get_current_server())
    # job_config.init_repo("https://github.com/bia1708/cimple.git", "bia1708", "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")
    # https://github.com/django/django.git
    # https://github.com/spring-projects/spring-petclinic.git
    # https://github.com/nlohmann/json.git
    # config.load_jobs()
    # config.close()

    app = QApplication()
    app.setApplicationName('cimple')

    window = MainWindow()

    app.setWindowIcon(QIcon("src/ui/resources/cimple.ico"))

    app.exec()

#curl jq gh python3.10-venv maven cmake
#TODO: PUT APT DEPS IN MAKEFILE
#TODO: ADD pip DEPS IN REQ.TXT
#TODO: make jenkins sudoer?
#TODO: Create setup.py with PyCharm

# Bad Tokens for testing:
#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
#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
#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
