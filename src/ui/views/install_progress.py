from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QLabel, QMessageBox
import multiprocessing
from ui.components.progress_bar import ProgressBar
from ui.components.message_box import MessageBox


class Worker(QThread):
    def __init__(self, config, username, password, proxy):
        super().__init__()
        self.config = config
        self.username = username
        self.password = password
        self.proxy = proxy

    def run(self):
        self.config.perform_fresh_install(self.username, self.password, self.proxy)


class InstallProgressView(QWidget):
    def __init__(self, configurator, username, password, proxy):
        super().__init__()
        self._configurator = configurator
        self._username = username
        self._password = password
        self._proxy = proxy

        self._heading_label = QLabel("Configuring Jenkins Setup")
        self._heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._heading_label.setStyleSheet('font-family: Inria Sans; font-size: 22px; text-align: center;')
        self._heading_label.setWordWrap(True)

        self._subheading_label = QLabel("This will take a while ...")
        self._subheading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subheading_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._subheading_label.setWordWrap(True)

        self.progress_bar = ProgressBar()
        self.progress_bar.setValue(0)

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self._heading_label)
        layout.addWidget(self._subheading_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
        self._configurator.install_signal.connect(self.update_progress)
        self.worker = Worker(self._configurator, self._username, self._password, self._proxy)
        self.worker.start()

    error_signal = Signal(str)

    def update_progress(self, progress, message):
        if progress != -1 :
            self.progress_bar.setValue(progress)
            text = self.info_label.text() + message
            self.info_label.setText(text)
            if progress == 0 and message == "Setting up proxy...\n":
                self._heading_label.setText("Configuring Proxy Service")
            if progress == 100 and self._proxy is not True:
                self.worker.terminate()
            elif progress == 100 and message == "Proxy setup complete":
                self.worker.terminate()
        else:
            self.worker.terminate()
            message_box = MessageBox()
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText(message)
            message_box.setWindowTitle("Error")
            message_box.buttonClicked.connect(lambda: self.error_signal.emit(message))
            message_box.exec()
