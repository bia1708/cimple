from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QLabel, QMessageBox
import multiprocessing
from ui.components.progress_bar import ProgressBar


class Worker(QThread):
    def __init__(self, config, username, password):
        super().__init__()
        self.config = config
        self.username = username
        self.password = password

    def run(self):
        self.config.perform_fresh_install(self.username, self.password)


class InstallProgressView(QWidget):
    def __init__(self, configurator, username, password):
        super().__init__()
        self._configurator = configurator

        self._heading_label = QLabel("Configuring Jenkins Setup")
        self._heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._heading_label.setStyleSheet('font-family: Inria Sans; font-size: 22px; text-align: center;')
        self._heading_label.setWordWrap(True)

        self._subheading_label = QLabel("This will take a while ...")
        self._subheading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subheading_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._subheading_label.setWordWrap(True)

        self.progressBar = ProgressBar()
        self.progressBar.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(self._heading_label)
        layout.addWidget(self._subheading_label)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)
        self._configurator.install_signal.connect(self.update_progress)
        self.worker = Worker(self._configurator, username, password)
        self.worker.start()

    def update_progress(self, progress, message):
        if progress != -1 and progress < 100:
            self.progressBar.setValue(progress)
            label = QLabel(message)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            self.layout().addWidget(label)
        elif progress == 100:
            self.worker.terminate()
        else:
            self.worker.terminate()
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText(message)
            message_box.setWindowTitle("Error")
            message_box.exec()
