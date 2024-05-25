from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

from src.ui.components.link_event import LinkEvent
from src.ui.components.message_box import MessageBox
from src.ui.components.progress_bar import ProgressBar


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

        self._hover_filter = LinkEvent()

        self._message_box = MessageBox()
        self._message_box.setTextFormat(Qt.TextFormat.RichText)
        self._message_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self._message_box.installEventFilter(self._hover_filter)

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
    change_view_signal = Signal(str)

    def update_progress(self, progress, message):
        if progress != -1:
            self.progress_bar.setValue(progress)
            text = self.info_label.text() + message
            self.info_label.setText(text)
            if progress == 0 and message == "Setting up proxy...\n":
                self._heading_label.setText("Configuring Proxy Service")
            if progress == 100:
                self.worker.terminate()

                link = "<a href=\"http://127.0.0.1:8080\" style='color: #81B622; text-decoration: none; font-size:16px;'>http://127.0.0.1:8080</a>"
                on_hover_link = "<a href=\"http://127.0.0.1:8080\" style='color: #81B622; text-decoration: underline; font-size:16px;'>http://127.0.0.1:8080</a>"
                text_with_link = "Jenkins setup complete.\nYou can view your Jenkins instance at " + link + "\nClick OK to proceed."
                text_with_hover_link = "Jenkins setup complete.\nYou can view your Jenkins instance at " + on_hover_link + "\nClick OK to proceed."
                self._hover_filter.set_link(text_with_link)
                self._hover_filter.set_on_hover_link(text_with_hover_link)
                self._message_box.setText(text_with_link)
                self._message_box.buttonClicked.connect(lambda: self.change_view_signal.emit("OK"))
                self._message_box.exec()
            # elif progress == 100 and message == "Proxy setup complete":
            #     self.worker.terminate()
            #     self._message_box.setText("Setup complete.\nYou can view your Jenkins instance at " +
            #                               "http://localhost:8080/\nClick OK to proceed.")
            #     self._message_box.buttonClicked.connect(lambda: self.change_view_signal.emit("OK"))
            #     self._message_box.exec()
        else:
            self.worker.terminate()
            self._message_box.setIcon(QMessageBox.Icon.Critical)
            self._message_box.setText(message)
            self._message_box.setWindowTitle("Error")
            self._message_box.buttonClicked.connect(lambda: self.error_signal.emit(message))
            self._message_box.exec()
