from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QCheckBox

from service.job_configurator import JobConfigurator
from ui.components.line_edit import LineEdit
from ui.components.button import Button


class CreateJobFormView(QWidget):
    def __init__(self, server):
        super().__init__()
        self._server = server
        self._job_configurator = JobConfigurator(self._server)
        self.setWindowTitle("cimple")
        self.resize(600, 350)

        # Create form widget
        self._form_widget = QWidget()

        # Repo url label + form
        self._repo_label = QLabel("Git Repository:")
        self._repo_line_edit = LineEdit()
        self._repo_line_edit.setPlaceholderText("Git Repository")
        self._repo_line_edit.textChanged.connect(self.check_input)

        # Username label + form
        self._username_label = QLabel("Git Username:")
        self._username_line_edit = LineEdit()
        self._username_line_edit.setPlaceholderText("Git Username")
        self._username_line_edit.textChanged.connect(self.check_input)

        # Password label + form
        self._token_label = QLabel("GitHub Token:")
        self._token_line_edit = LineEdit()
        self._token_line_edit.setPlaceholderText("GitHub Token")
        self._token_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._token_line_edit.textChanged.connect(self.check_input)

        self._checkbox = QCheckBox("Enable GitHub Job Status")
        self._checkbox.stateChanged.connect(lambda: (
                self._next_button.setEnabled(False),
                self.check_input()
            ))

        # Next button which sends a signal to the main window object to perform the fresh install
        self._next_button = Button("Next")
        self._next_button.setEnabled(False)
        self._next_button.pressed.connect(self.next_button_action)

        # Save the form widgets in a separate widget which has QFormLayout (it looks better)
        layout = QFormLayout()
        layout.addRow(self._username_label, self._username_line_edit)
        layout.addRow(self._token_label, self._token_line_edit)
        self._error_label = QLabel()
        self._error_label.setStyleSheet("color: red;")
        self._error_label.setVisible(False)
        # self._job_configurator.auth_signal.connect(self.show_error)
        layout.addWidget(self._checkbox)
        layout.addWidget(self._error_label)
        layout.addWidget(self._next_button)
        self._form_widget.setLayout(layout)

        # Create outer layout: Install form label + Form widget
        outer_layout = QVBoxLayout()
        self._label = QLabel("Please enter your GitHub credentials:")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._label.setWordWrap(True)
        outer_layout.addWidget(self._label)
        outer_layout.addWidget(self._form_widget)
        self.setLayout(outer_layout)
        self.show()

    # Signal which send the username and password to MainWindow
    form_signal = Signal(str, str, bool)

    def check_input(self):
        username = self._username_line_edit.text().strip()
        token = self._token_line_edit.text().strip()
        permissions = True
        auth = False
        if bool(username) and bool(token):
            auth = self.validate_token(token)
            if auth is False:
                self.show_error(1, "Wrong auth")
        if self._checkbox.isChecked():
            permissions = self.validate_permissions(token)
            if permissions is False:
                self.show_error(1, "No permissions")
        self._next_button.setEnabled(auth and permissions)

    def next_button_action(self):
        self.form_signal.emit(self._username_line_edit.text(), self._token_line_edit.text(), self._checkbox.isChecked())

    def validate_token(self, token):
        return self._job_configurator.validate_gh_credentials(token)

    def validate_permissions(self, token):
        return self._job_configurator.validate_token_permissions(token)

    def show_error(self, error_code, message):
        if error_code != 0:
            print("HEHE")
            self._error_label.setText(message)
            self._error_label.setVisible(True)
