from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

from service.configurator import Configurator
from service.job_configurator import Job_Configurator

from ui.main_window import MainWindow

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
    # config.load_jobs()
    # config.close()

    app = QApplication()
    app.setApplicationName('cimple')

    window = MainWindow()

    app.setWindowIcon(QIcon("ui/resources/cimple.ico"))

    app.exec()

#curl jq gh python3.10-venv
#TODO: PUT APT DEPS IN MAKEFILE
#TODO: ADD pip DEPS IN REQ.TXT
#TODO: make jenkins sudoer?
#TODO: Create setup.py with PyCharm
