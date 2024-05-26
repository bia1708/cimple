"""
@Author: Bianca Popu (bia1708)
@Date: 27/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
import os

from PySide6.QtCore import Qt, Signal, QThreadPool, QObject, QRunnable, QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QCheckBox

from src.service.job_configurator import JobConfigurator
from src.ui.components.button import Button
from src.ui.components.line_edit import LineEdit


class JobCreationWorker(QThread):
    """
    Worker Thread Class for creating jobs.
    :ivar config: `JobConfigurator` instance
    :ivar repo: `str` repository URL
    :ivar username: `str` git username
    :ivar token: `str` git token
    :ivar git_status: `boolean` True if GitHub integration is enabled
    :ivar finished_signal: `Signal` signal when the thread is finished
    """
    def __init__(self, config, repo, username, token, git_status):
        super().__init__()
        self.repo = repo
        self.config = config
        self.username = username
        self.token = token
        self.git_status = git_status

    finished_signal = Signal(bool)

    def run(self):
        """
        Runs the worker thread, which creates a job and emits a signal when finished.
        :return:
        """
        self.config.init_repo(self.repo, self.username, self.token, self.git_status)
        self.finished_signal.emit(True)


class WorkerSignal(QObject):
    """
    Worker Signal Class to emit thread results. Used inside the thread pool when a thread is finished.
    :ivar result_signal: `Signal` signal when a thread is finished
    """
    result_signal = Signal(bool, bool, bool)


class Worker(QRunnable):
    """
    Worker Class for validating credentials.
    :param config: `JobConfigurator` instance
    :param repo: `str` repository URL
    :param username: `str` git username
    :param token: `str` git token
    :param git_status: `boolean` True if GitHub integration is enabled
    :ivar config: `JobConfigurator` instance
    :ivar repo: `str` repository URL
    :ivar username: `str` git username
    :ivar token: `str` git token
    :ivar git_status: `boolean` True if GitHub integration is enabled
    """
    def __init__(self, config, username, token, git_status, repo):
        super().__init__()
        self.config = config
        self.username = username
        self.token = token
        self.git_status = git_status
        self.repo = repo
        self.signal = WorkerSignal()

    def run(self):
        """
        Function to run the worker thread. It validates the credentials and creates a job and emits a signal when
        finished.
        """
        auth = self.config.validate_gh_credentials(self.token, self.username)
        if auth:
            repo = self.config.validate_repo_exists(self.username, self.repo)
        permissions = not self.git_status
        if self.git_status is True:
            permissions = self.config.validate_token_permissions(self.token)
        self.signal.result_signal.emit(auth, permissions, repo)


class CreateJobFormView(QWidget):
    """
    CreateJobForm View Class
    :ivar _server: `Server` instance, current server
    :ivar _job_configurator: `JobConfigurator` instance
    :ivar thread_pool: `QThreadPool` instance
    :ivar _form_widget: `QFormLayout` instance
    :ivar _repo_label: `QLabel` repository label
    :ivar _repo_line_edit: `QLineEdit` repository line edit
    :ivar _username_label: `QLabel` username label
    :ivar _username_line_edit: `QLineEdit` username line edit
    :ivar _token_label: `QLabel` token label
    :ivar _token_line_edit: `QLineEdit` token line edit
    :ivar _checkbox: `QCheckBox` checkbox for GitHub Integration
    :ivar _next_button: `QPushButton` next button
    :ivar _error_label: `QLabel` error label
    :ivar _label: `QLabel` window title label
    :ivar form_signal: `Signal` signal to communicate with MainWindow
    """
    def __init__(self, server):
        super().__init__()
        self._server = server
        self._job_configurator = JobConfigurator(self._server)
        self.setWindowTitle("cimple")
        self.resize(600, 350)

        self.thread_pool = QThreadPool()

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

        self._checkbox = QCheckBox("Enable GitHub Integration")
        if os.path.isfile("/etc/systemd/system/smee.service") is False:
            self._checkbox.setEnabled(False)
        self._checkbox.stateChanged.connect(lambda: (
                self._next_button.setEnabled(False),
                self.check_input()
            ))

        # Next button which sends a signal to the main window object to perform the fresh install
        self._next_button = Button("Create")
        self._next_button.setEnabled(False)
        self._next_button.pressed.connect(self.next_button_action)

        # Save the form widgets in a separate widget which has QFormLayout (it looks better)
        layout = QFormLayout()
        layout.addRow(self._username_label, self._username_line_edit)
        layout.addRow(self._token_label, self._token_line_edit)
        layout.addRow(self._repo_label, self._repo_line_edit)
        self._error_label = QLabel("")
        self._error_label.setStyleSheet("color: red;")
        # self._error_label.setVisible(False)
        self._job_configurator.auth_signal.connect(self.show_error)
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
        """
        Function which validates user credentials. It spawns a thread from the thread pool to validate credentials.
        """
        username = self._username_line_edit.text().strip()
        token = self._token_line_edit.text().strip()
        repo = self._repo_line_edit.text().strip()
        if bool(username) and bool(token) and bool(repo):
            self.setCursor(Qt.CursorShape.BusyCursor)
            worker = Worker(self._job_configurator, username, token, self._checkbox.isChecked(), repo)
            worker.signal.result_signal.connect(self.enable_next)
            self.thread_pool.start(worker)

    def enable_next(self, auth, permissions, repo):
        """
        Function which determines whether the "Next" button should be enabled and then enables it
        :param auth: `boolean` result of credentials verification
        :param permissions: `boolean` result of permissions verification
        :param repo: `boolean` result of repository verification
        """
        self._next_button.setEnabled(auth and permissions and repo)

    def next_button_action(self):
        """
        Function which handles the "Next" button press. When the "Next" button is pressed, spawn a single thread which
        handles job creation. Close this view after thread is spawned, to not make the user wait for the job to finish.
        """
        self.job_worker = JobCreationWorker(self._job_configurator, self._repo_line_edit.text(),
                                            self._username_line_edit.text(), self._token_line_edit.text(),
                                            self._checkbox.isChecked())
        self.job_worker.finished_signal.connect(self.finished_job_creation)
        self.job_worker.start()
        self.close()

    def show_error(self, error_code, message):
        """
        Function which is executed when one of the validations fails. The _error_label is populated with the error
        message.
        :param error_code: `int` error code
        :param message: `str` error message
        """
        if error_code != 0:
            self._error_label.setText(message)
        else:
            self._error_label.setText("")

    def finished_job_creation(self, status):
        """
        Function which kills the thread after the job has been created.
        :param status: `int` status code
        """
        if status:
            self.job_worker.terminate()
