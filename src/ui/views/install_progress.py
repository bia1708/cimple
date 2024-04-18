from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QLabel
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
        #total_iterations = 100

        #for i in range(total_iterations):
            # Simulating work
            # Replace this with your actual code
            # Update progress
            #self.progress_callback.emit(i * 100 / total_iterations)
            # Simulate some delay
            #self.sleep(0.1)
        #self.progress_callback(10)

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
        self._configurator.install_signal.connect(self.progressBar.setValue,
                                                  Qt.ConnectionType.QueuedConnection)
        self.worker = Worker(self._configurator,
                             username, password)
        self.worker.start()
        #self.update_progress(90)
        #self._configurator.perform_fresh_install(username, password)

    def update_progress(self, progress):
        print(progress)
        print(type(progress))
        progress = 10
        print(type(progress))
        self.progressBar.setValue(progress)
        print("HERE")

