"""
@Author: Bianca Popu (bia1708)
@Date: 17/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

from src.ui.components.link_event import LinkEvent
from src.ui.components.message_box import MessageBox
from src.ui.components.progress_bar import ProgressBar


class Worker(QThread):
    """
    Worker Thread Class which performs the fresh install functionality.
    :param config: `Configurator` instance
    :param username: `str` Jenkins username
    :param password: `str` Jenkins password
    :param proxy: `boolean` True if proxy setup is enabled
    :ivar config: `Configurator` instance
    :ivar username: `str` Jenkins username
    :ivar password: `str` Jenkins password
    :ivar proxy: `boolean` True if proxy setup is enabled
    """
    def __init__(self, config, username, password, proxy):
        super().__init__()
        self.config = config
        self.username = username
        self.password = password
        self.proxy = proxy

    def run(self):
        """
        Function which runs the worker thread (performs the fresh install functionality).
        """
        self.config.perform_fresh_install(self.username, self.password, self.proxy)


class InstallProgressView(QWidget):
    """
    Install Progress View Class
    :param configurator: `Configurator` instance
    :param username: `str` Jenkins username
    :param password: `str` Jenkins password
    :param proxy: `boolean` True if proxy setup is enabled
    :ivar _configurator: `Configurator` instance
    :ivar _username: `str` Jenkins username
    :ivar _password: `str` Jenkins password
    :ivar _proxy: `boolean` True if proxy setup is enabled
    :ivar _hover_filter: `LinkEvent` instance
    :ivar _message_box: `MessageBox` instance for notifying user about finish status
    :ivar _heading_label: `QLabel` heading label
    :ivar _subheading_label: `QLabel` subheading label
    :ivar _progress_bar: `ProgressBar` instance for install progress
    :ivar _info_label: `QLabel` info label for install steps
    :ivar error_signal: `Signal` instance for notifying user about errors
    :ivar change_view_signal: `Signal` instance for notifying MainWindow to change view
    """
    def __init__(self, configurator, username, password, proxy):
        super().__init__()
        self._configurator = configurator
        self._username = username
        self._password = password
        self._proxy = proxy

        # Link event for hovering over links (the message box link)
        self._hover_filter = LinkEvent()

        # Message box for install status (error/success)
        self._message_box = MessageBox()
        self._message_box.setTextFormat(Qt.TextFormat.RichText)
        self._message_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self._message_box.installEventFilter(self._hover_filter)

        # Window title label
        self._heading_label = QLabel("Configuring Jenkins Setup")
        self._heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._heading_label.setStyleSheet('font-family: Inria Sans; font-size: 22px; text-align: center;')
        self._heading_label.setWordWrap(True)

        # Window subtitle label
        self._subheading_label = QLabel("This will take a while ...")
        self._subheading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subheading_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._subheading_label.setWordWrap(True)

        # Progress bar for install progress
        self._progress_bar = ProgressBar()
        self._progress_bar.setValue(0)

        # Info label which is populated with current installation step
        self._info_label = QLabel("")
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._info_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self._heading_label)
        layout.addWidget(self._subheading_label)
        layout.addWidget(self._progress_bar)
        layout.addWidget(self._info_label)
        self.setLayout(layout)

        # Start the installation as soon as the window is created and connect the configurator signal to the
        # update_progress function which updates the progress bar + info label
        self._configurator.install_signal.connect(self.update_progress)
        self.worker = Worker(self._configurator, self._username, self._password, self._proxy)
        self.worker.start()

    error_signal = Signal(str)
    change_view_signal = Signal(str)

    def update_progress(self, progress, message):
        """
        Function which updates the progress bar and info label based on installation progress.
        :param progress: `int` progress percentage
        :param message: `str` info message to be displayed
        """
        # -1 is the default error code used
        if progress != -1:
            self._progress_bar.setValue(progress)
            text = self._info_label.text() + message
            self._info_label.setText(text)
            # If the user enabled proxy at this step, change the heading and reset progress bar
            if progress == 0 and message == "Setting up proxy...\n":
                self._heading_label.setText("Configuring Proxy Service")
            # If progress got to 100, display "Success" message box with clickable link and kill thread. Change view on
            # OK button click
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
        else:
            # If the install hangs with errors, display "Error" message box and notify the MainWindow to send the user
            # back to the homepage
            self.worker.terminate()
            self._message_box.setIcon(QMessageBox.Icon.Critical)
            self._message_box.setText(message)
            self._message_box.setWindowTitle("Error")
            self._message_box.buttonClicked.connect(lambda: self.error_signal.emit(message))
            self._message_box.exec()
