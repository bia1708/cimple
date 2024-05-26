"""
@Author: Bianca Popu (bia1708)
@Date: 29/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QMessageBox, QCheckBox

from src.ui.components.button import Button
from src.ui.components.line_edit import LineEdit
from src.ui.components.message_box import MessageBox


class Worker(QThread):
    """
    Worker Thread Class for connecting to server.
    :param config: `Configurator` instance
    :param username: `str` Jenkins username
    :param password: `str` Jenkins password
    :param url: `str` Jenkins URL
    :param plugins: `boolean` True if downloading plugins is enabled
    :ivar config: `Configurator` instance
    :ivar username: `str` Jenkins username
    :ivar password: `str` Jenkins password
    :ivar url: `str` Jenkins URL
    :ivar plugins: `boolean` True if downloading plugins is enabled
    :ivar finished_signal: `Signal` signal when the worker thread is finished
    """
    def __init__(self, config, username, password, url, plugins):
        super().__init__()
        self.config = config
        self.config.connect_signal.connect(self.emit_signal)
        self.username = username
        self.password = password
        self.url = url
        self.plugins = plugins

    finished_signal = Signal(int, str)

    def run(self):
        """
        Method that runs the worker thread. The thread calls the connect function inside the Configurator class.
        """
        self.config.connect_to_existing_jenkins(self.username, self.password, self.url, self.plugins)

    def emit_signal(self, status, msg):
        """
        Function which emits a signal when the thread is finished
        :param status: `int` status code
        :param msg: `str` message
        """
        self.finished_signal.emit(status, msg)


class ConnectToServerFormView(QWidget):
    """
    View class for connecting to server.
    :param configurator: `Configurator` instance
    :ivar _configurator: `Configurator` instance
    :ivar _form_widget: `QFormLayout` instance
    :ivar _username_label: `QLabel` label for username
    :ivar _username_line_edit: `QLineEdit` label for username
    :ivar _password_label: `QLabel` label for password
    :ivar _password_line_edit: `QLineEdit` label for password
    :ivar _url_label: `QLabel` label for url
    :ivar _url_line_edit: `QLineEdit` label for url
    :ivar _checkbox: `QCheckBox` checkbox for installing recommended plugins
    :ivar _next_button: `QPushButton` button for next step
    :ivar _label: `QLabel` label for window title
    :ivar _message_box: `QMessageBox` messagebox for error notifications
    :ivar finished_signal: `Signal` signal to notify the MainWindow
    """
    def __init__(self, configurator):
        super().__init__()
        # Create form widget
        self._configurator = configurator
        self._form_widget = QWidget()
        self.setWindowTitle("cimple")
        self.resize(600, 350)
        self.show()

        # Username label + form
        self._username_label = QLabel("Username:")
        self._username_line_edit = LineEdit()
        self._username_line_edit.setPlaceholderText("Username")
        self._username_line_edit.textChanged.connect(self.check_input)

        # Password label + form
        self._password_label = QLabel("Password:")
        self._password_line_edit = LineEdit()
        self._password_line_edit.setPlaceholderText("Password")
        self._password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_line_edit.textChanged.connect(self.check_input)

        # URL label + form
        self._url_label = QLabel("Jenkins URL:")
        self._url_line_edit = LineEdit()
        self._url_line_edit.setPlaceholderText("Jenkins URL")
        self._url_line_edit.textChanged.connect(self.check_input)

        # Install recommended plugins checkbox
        self._checkbox = QCheckBox("Install recommended plugins on remote server")

        # Next button which sends a signal to the main window object to perform the fresh install
        self._next_button = Button("Next")
        self._next_button.setEnabled(False)
        self._next_button.clicked.connect(self.next_button_action)

        # Save the form widgets in a separate widget which has QFormLayout (it looks better)
        layout = QFormLayout()
        layout.addRow(self._username_label, self._username_line_edit)
        layout.addRow(self._url_label, self._url_line_edit)
        layout.addRow(self._password_label, self._password_line_edit)
        layout.addWidget(self._checkbox)
        layout.addWidget(self._next_button)
        self._form_widget.setLayout(layout)

        # Create outer layout: Install form label + Form widget
        outer_layout = QVBoxLayout()
        self._label = QLabel("Please enter your remote Jenkins credentials:")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._label.setWordWrap(True)
        outer_layout.addWidget(self._label)
        outer_layout.addWidget(self._form_widget)
        self.setLayout(outer_layout)
        self._message_box = MessageBox()

    # Signal which send the username and password to MainWindow
    finished_signal = Signal(int, str)

    def check_input(self):
        """
        Function which validates user input before enabling the "Next" button.
        """
        username = self._username_line_edit.text().strip()
        password = self._password_line_edit.text().strip()
        url = self._url_line_edit.text().strip()
        # Enable the button only if username, password and url are not empty
        self._next_button.setEnabled(bool(username) and bool(password) and bool(url))

    def next_button_action(self):
        """
        Function which begins the "Connect to Server" function by launching a worker thread.
        """
        self.setCursor(Qt.CursorShape.BusyCursor)
        self.worker = Worker(self._configurator, self._username_line_edit.text(), self._password_line_edit.text(),
                             self._url_line_edit.text(), self._checkbox.isChecked())
        self.worker.start()
        self.worker.finished_signal.connect(self.finish_connect)

    def finish_connect(self, status, msg):
        """
        Function which executes when the worker thread is finished. If there are any errors, it spawns a message box
        containing the error. This view then closes itself.
        :param status: `int` status code
        :param msg: `str` message
        """
        if status != 1:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self._message_box.setIcon(QMessageBox.Icon.Critical)
            self._message_box.setText(msg)
            self._message_box.setWindowTitle("Error")
            self._message_box.exec()

        self.finished_signal.emit(status, msg)
        self.close()
