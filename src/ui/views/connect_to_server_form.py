from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QMessageBox, QCheckBox

from src.ui.components.message_box import MessageBox
from src.ui.components.line_edit import LineEdit
from src.ui.components.button import Button


class Worker(QThread):
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
        self.config.connect_to_existing_jenkins(self.username, self.password, self.url, self.plugins)
        # self.finished_signal.emit(status)
        
    def emit_signal(self, status, msg):
        print(msg)
        self.finished_signal.emit(status, msg)


class ConnectToServerFormView(QWidget):
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

        # Username label + form
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
        username = self._username_line_edit.text().strip()
        password = self._password_line_edit.text().strip()
        url = self._url_line_edit.text().strip()
        # Enable the button only if username, password and url are not empty
        self._next_button.setEnabled(bool(username) and bool(password) and bool(url))

    def next_button_action(self):
        self.setCursor(Qt.CursorShape.BusyCursor)
        self.worker = Worker(self._configurator, self._username_line_edit.text(), self._password_line_edit.text(), self._url_line_edit.text(), self._checkbox.isChecked())
        self.worker.start()
        self.worker.finished_signal.connect(self.finish_connect)

    def finish_connect(self, status, msg):
        if status != 1:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self._message_box.setIcon(QMessageBox.Icon.Critical)
            self._message_box.setText(msg)
            self._message_box.setWindowTitle("Error")
            # self._message_box.buttonClicked.connect(lambda: self.error_signal.emit(message))
            self._message_box.exec()

        self.finished_signal.emit(status, msg)
        self.close()
