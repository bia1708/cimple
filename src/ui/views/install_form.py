"""
@Author: Bianca Popu (bia1708)
@Date: 17/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QCheckBox

from src.ui.components.button import Button
from src.ui.components.line_edit import LineEdit


class InstallFormView(QWidget):
    """
    InstallForm View Class
    :ivar _form_widget: `QWidget` form widget to be displayed
    :ivar _username_label: `QLabel` username label
    :ivar _username_line_edit: `QLineEdit` username line
    :ivar _password_label: `QLabel` password label
    :ivar _password_line_edit: `QLineEdit` password line
    :ivar _checkbox: `QCheckBox` checkbox for setting up proxy service
    :ivar _next_button: `QPushButton` next button
    :ivar _label: `QLabel` window title label
    :ivar form_signal: `Signal` signal to send to MainWindow when form is created
    """
    def __init__(self):
        super().__init__()
        # Create form widget
        self._form_widget = QWidget()

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

        self._checkbox = QCheckBox("Enable Reverse Proxy Service")

        # Next button which sends a signal to the main window object to perform the fresh install
        self._next_button = Button("Next")
        self._next_button.setEnabled(False)
        self._next_button.pressed.connect(self.next_button_action)

        # Save the form widgets in a separate widget which has QFormLayout (it looks better)
        layout = QFormLayout()
        layout.addRow(self._username_label, self._username_line_edit)
        layout.addRow(self._password_label, self._password_line_edit)
        layout.addWidget(self._checkbox)
        layout.addWidget(self._next_button)
        self._form_widget.setLayout(layout)

        # Create outer layout: Install form label + Form widget
        outer_layout = QVBoxLayout()
        self._label = QLabel("Please enter your Jenkins credentials:")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._label.setWordWrap(True)
        outer_layout.addWidget(self._label)
        outer_layout.addWidget(self._form_widget)
        self.setLayout(outer_layout)

    # Signal which send the username and password to MainWindow
    form_signal = Signal(str, str, bool)

    def check_input(self):
        """
        Function to check user input before enabling the next button.
        """
        username = self._username_line_edit.text().strip()
        password = self._password_line_edit.text().strip()
        # Enable the button only if both username and password are not empty
        self._next_button.setEnabled(bool(username) and bool(password))

    def next_button_action(self):
        """
        Function to notify the MainWindow that the form has been created.
        """
        self.form_signal.emit(self._username_line_edit.text(), self._password_line_edit.text(), self._checkbox.isChecked())
