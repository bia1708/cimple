"""
@Author: Bianca Popu (bia1708)
@Date: 21/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
import os

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QTableWidgetItem, QSpacerItem, \
    QSizePolicy, QMessageBox

from src.service.job_configurator import JobConfigurator
from src.ui.components.button import Button
from src.ui.components.link_event import LinkEvent
from src.ui.components.list_view import ListView
from src.ui.components.message_box import MessageBox
from src.ui.components.table import Table
from src.ui.views.connect_to_server_form import ConnectToServerFormView
from src.ui.views.create_job_form import CreateJobFormView


class RunJobWorker(QThread):
    """
    Worker Thread Class used to run jobs.
    :param config: `JobConfigurator` instance
    :param job: `str` job name
    :ivar config: `JobConfigurator` instance
    :ivar job: `str` job name
    :ivar finished_signal: `Signal` to notify when worker is finished
    """
    def __init__(self, config, job):
        super().__init__()
        self.config = config
        self.job = job

    finished_signal = Signal(bool)

    def run(self):
        """
        Function which triggers a given job. Emits a signal to notify when finished.
        """
        job_configurator = JobConfigurator(self.config.get_current_server())
        job_configurator.run_job(self.job)
        self.finished_signal.emit(True)


class EnableProxyWorker(QThread):
    """
    Worker Thread Class used to enable proxy.
    :param config: `JobConfigurator` instance
    :ivar config: `JobConfigurator` instance
    :ivar finished_signal: `Signal` to notify when worker is finished
    """
    def __init__(self, config):
        super().__init__()
        self.config = config

    finished_signal = Signal(bool, int)

    def run(self):
        """
        Function which enables proxy. Emits a signal to notify when finished.
        """
        status = self.config.enable_proxy()
        self.finished_signal.emit(True, status)


class InstallPluginsWorker(QThread):
    """
    Worker Thread Class used to install plugins.
    :param config: `JobConfigurator` instance
    :ivar config: `JobConfigurator` instance
    :ivar finished_signal: `Signal` to notify when worker is finished
    """
    def __init__(self, config):
        super().__init__()
        self.config = config

    finished_signal = Signal(bool)

    def run(self):
        """
        Function which enables plugins. Emits a signal to notify when finished.
        """
        current_server = self.config.get_current_server()
        self.config.install_plugins(current_server.get_username(), current_server.get_token(), current_server.get_jnlp_file(), current_server.get_url())
        self.finished_signal.emit(True)


class ItemsView(QWidget):
    """
    Items View Class. This is the main functional window for the application.
    :param configurator: `Configurator` instance
    :ivar _configurator: `Configurator` instance
    :ivar _splitter: `QSplitter` instance for splitting left and right columns
    :ivar _left_column: `QWidget` instance for left column
    :ivar _server_list_label: `QLabel` label for server list column title
    :ivar _server_list:`QListWidget` items for server list column
    :ivar _server_list_view: `QListView` view for server list column
    :ivar _left_column_layout: `QVBoxLayout` layout for left column widget
    :ivar _right_column: `QWidget` instance for right column widget
    :ivar _right_column_layout: `QVBoxLayout` layout for right column widget
    :ivar _current_server_label: `QLabel` label for current server URL
    :ivar _hover_filter: `LinkEvent` instance for hover events
    :ivar _jobs_table: `Table` instance for jobs table
    :ivar timer: `QTimer` instance for jobs table update cooldown
    :ivar _buttons_container: `QWidget` layout for buttons container
    :ivar _buttons_container_layout: `QVBoxLayout` layout for buttons container
    :ivar _connect_to_server_button: `Button` button for connecting to server
    :ivar _run_job_button: `Button` button for running a selected job
    :ivar _fresh_install_button: `Button` button for installing Jenkins
    :ivar _enable_proxy_button: `Button` button for enabling proxy
    :ivar _install_plugins_button: `Button` button for installing plugins
    :ivar _view_layout: `QVBoxLayout` layout for view widget
    :ivar fresh_install_signal: `Signal` signal to notify when fresh install is triggered
    """
    def __init__(self, configurator):
        super().__init__()

        self._configurator = configurator
        self._splitter = QSplitter(Qt.Horizontal)

        # Left column contains the server list
        self._left_column = QWidget()

        # Server list title
        self._server_list_label = QLabel("Server List")
        self._server_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._server_list_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._server_list_label.setWordWrap(True)

        # Server list view model and selection behaviour
        self._server_list_view = ListView()
        self._server_list = QtGui.QStandardItemModel()
        self.update_servers_list()
        self._server_list_view.setModel(self._server_list)
        selection_model = self._server_list_view.selectionModel()
        selection_model.selectionChanged.connect(self.set_new_current_server)

        # Set the default selected item to be the last connected server
        default_index = self.find_index_by_url(self._configurator.get_current_server().get_url())  # Get the index of the first row
        selection_model.select(
            default_index, QtCore.QItemSelectionModel.SelectionFlag.Select
        )

        # Construct left column
        self._left_column_layout = QVBoxLayout()
        self._left_column_layout.setContentsMargins(0, 0, 0, 0)
        self._left_column_layout.setSpacing(10)
        self._left_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add widgets to left column
        self._left_column_layout.addWidget(self._server_list_label)
        self._left_column_layout.addWidget(self._server_list_view)
        self._left_column.setLayout(self._left_column_layout)

        # Right column contains:
        #   - jobs table
        #   - connect-to-server button
        #   - enable-proxy button
        #   - fresh-install button
        #   - install-plugins button
        #   - run-job button
        #   - create-job button
        self._right_column = QWidget()
        self._right_column_layout = QVBoxLayout()
        self._right_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set the current server label to the current server link and make it clickable
        self._current_server_label = QLabel()
        self._current_server_label.setTextFormat(Qt.TextFormat.RichText)
        self._current_server_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self._current_server_label.setOpenExternalLinks(True)
        self._hover_filter = LinkEvent()
        self._current_server_label.installEventFilter(self._hover_filter)
        self._current_server_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self._current_server_label.setWordWrap(True)
        self._current_server_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_current_server_label()

        # Create a table to display the list of jobs for the current server
        self._jobs_table = Table()  # Rows and columns
        self._jobs_table.setHorizontalHeaderLabels(["My Jobs", "No. of Builds", "Status", "GitHub Integration"])
        self._jobs_table.selectionModel().selectionChanged.connect(self.table_selection_event)

        self.update_jobs_table()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_jobs_table)
        self.timer.start(7000)

        # Create job button + Connect to server button
        self._buttons_container = QWidget()
        self._buttons_container.setContentsMargins(0, 0, 0, 0)
        self._buttons_container_layout = QHBoxLayout()
        self._buttons_container.setLayout(self._buttons_container_layout)

        # Add job button
        self._add_job_button = Button("Create Job")
        self._add_job_button.clicked.connect(self.show_create_job_view)

        # Connect to server button
        self._connect_to_server_button = Button("Connect to Server")
        self._connect_to_server_button.clicked.connect(self.show_connect_to_server_view)

        # Run job button
        self._run_job_button = Button("Run Job")
        self._run_job_button.setContentsMargins(0, 0, 0, 0)
        self._run_job_button.setEnabled(False)
        self._run_job_button.clicked.connect(self.run_job)
        self._buttons_container_layout.addWidget(self._connect_to_server_button)

        # Fresh install button should only be visible if fresh install hasn't been performed yet
        if self._configurator.get_server_by_url("http://127.0.0.1:8080") is None and self._configurator.get_server_by_url("http://localhost:8080") is None:
            self._fresh_install_button = Button("Fresh Install")
            self._fresh_install_button.clicked.connect(lambda: self.fresh_install_signal.emit(True))
            self._buttons_container_layout.addWidget(self._fresh_install_button)

        # Enable proxy button should only be visible if the current server is the local one
        if os.path.isfile("/etc/systemd/system/smee.service") is False and (self._configurator.get_current_server().get_url() == "http://127.0.0.1:8080" or self._configurator.get_current_server().get_url() == "http://localhost:8080"):
            self._enable_proxy_button = Button("Enable Proxy")
            self._enable_proxy_button.clicked.connect(self.enable_proxy)
            self._buttons_container_layout.addWidget(self._enable_proxy_button)
            self.show_enable_proxy(self._configurator.get_current_server().get_url())
        # Install plugins button is available on all servers, at any time (useful for updating plugins as well)
        self._install_plugins_button = Button("Install Plugins")
        self._install_plugins_button.clicked.connect(self.install_plugins)

        # Add remaining components to buttons widget
        self._buttons_container_layout.addWidget(self._install_plugins_button)
        self._buttons_container_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self._buttons_container_layout.addWidget(self._run_job_button)
        self._buttons_container_layout.addWidget(self._add_job_button)

        # Right column: Title label, table with jobs, buttons widget
        self._right_column_layout.addWidget(self._current_server_label)
        self._right_column_layout.addWidget(self._jobs_table)
        self._right_column_layout.addWidget(self._buttons_container)
        self._right_column_layout.setSpacing(20)
        self._right_column.setLayout(self._right_column_layout)

        # Split left and right columns
        self._splitter.addWidget(self._left_column)
        self._splitter.addWidget(self._right_column)
        self._splitter.setSizes([300, 700])
        self._view_layout = QHBoxLayout()
        self._view_layout.addWidget(self._splitter)
        self.setLayout(self._view_layout)

    # Signal which signals to main window that fresh install should be performed
    fresh_install_signal = Signal(bool)

    def table_selection_event(self, selected, deselected):
        """
        Function which enables the "Run Job" button only when a job is selected.
        :param selected: `True` if a job is selected, `False` otherwise.
        :param deselected: `True` if a job is deselected, `False` otherwise.
        """
        if selected.indexes():
            self._run_job_button.setEnabled(True)
        else:
            self._run_job_button.setEnabled(False)

    def run_job(self):
        """
        Function which performs runs the "RunJobWorker" based on the selected job.
        """
        selected_indexes = self._jobs_table.selectionModel().selectedRows()

        if selected_indexes:
            selected_row = selected_indexes[0].row()  # Get the index of the selected row
            row_items = [self._jobs_table.item(selected_row, col).text() for col in range(self._jobs_table.columnCount())]

            print("Selected Row Items:", row_items)
            self.job_worker = RunJobWorker(self._configurator, row_items[0])
            self.job_worker.finished_signal.connect(lambda: self.job_worker.terminate())
            self.job_worker.start()

    def enable_proxy(self):
        """
        Function which starts a worker process for the "Enable Proxy" functionality.
        """
        self.setCursor(Qt.CursorShape.BusyCursor)
        self.proxy_worker = EnableProxyWorker(self._configurator)
        self.proxy_worker.finished_signal.connect(self.finish_enable_proxy)
        self.proxy_worker.start()

    def finish_enable_proxy(self, finished, status):
        """
        Function which hides the "Enable Proxy" button when the "Enable Proxy" functionality is done, or spawns an error
        MessageBox if there are any errors.
        :param finished: `boolean` True if worker process is finished, `False` otherwise.
        :param status: `int` The status code of the "Enable Proxy" worker.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.proxy_worker.terminate()
        if status == 0:
            self._enable_proxy_button.hide()
        else:
            self._message_box = MessageBox()
            self._message_box.setIcon(QMessageBox.Icon.Critical)
            self._message_box.setText("Failed to setup reverse proxy service!")
            self._message_box.setWindowTitle("Error")
            self._message_box.exec()

    def install_plugins(self):
        """
        Function which starts a worker process that installs plugins.
        """
        self.setCursor(Qt.CursorShape.BusyCursor)
        self.plugins_worker = InstallPluginsWorker(self._configurator)
        self.plugins_worker.finished_signal.connect(self.finish_install_plugins)
        self.plugins_worker.start()

    def finish_install_plugins(self):
        """
        Function which changes the cursor after plugins are installed.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.plugins_worker.terminate()

    def update_servers_list(self):
        """
        Function which updates the servers list with the current servers.
        """
        self._server_list.clear()
        servers = self._configurator.get_all_servers()
        for server in servers:
            server_item = QtGui.QStandardItem(server.get_url())
            server_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            server_item.setEditable(False)
            self._server_list.appendRow(server_item)

    def update_jobs_table(self):
        """
        Function which updates the jobs table with the current jobs. If job details are changed, modify only the
        affected table cells.
        """
        # Get current contents first
        current_rows = []
        jobs = self._configurator.load_jobs()

        # Filter out rows that need to be removed
        rows_to_remove = []
        job_titles = [x[0] for x in jobs]
        for row in range(self._jobs_table.rowCount()):
            item = self._jobs_table.item(row, 0)
            if item is not None and item.text() not in job_titles:
                rows_to_remove.append(row)

        # Remove rows from the table
        for row_index in reversed(rows_to_remove):
            self._jobs_table.removeRow(row_index)

        for row in range(self._jobs_table.rowCount()):
            current_row = []
            for col in range(self._jobs_table.columnCount()):
                item = self._jobs_table.item(row, col)
                if item is not None:
                    current_row.append(item.text())
                else:
                    current_row.append(None)
            current_rows.append(current_row)

        # Populate the table with job data from the current server
        for row_index, job_data in enumerate(jobs):
            if job_data not in current_rows:
                job_titles = [x[0] for x in current_rows]
                if job_data[0] not in job_titles:
                    self._jobs_table.insertRow(row_index)
                for col_index, col_data in enumerate(job_data):
                    item = QTableWidgetItem(col_data)
                    item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    item.setData(Qt.ItemDataRole.BackgroundRole, (job_data[4], job_data[5]))
                    self._jobs_table.setItem(row_index, col_index, item)

    def update_jobs_table_for_new_server(self):
        """
        Function which updates the jobs table when a new server is added (optimization for new servers).
        """
        # Clear contents first
        self._jobs_table.setRowCount(0)

        jobs = self._configurator.load_jobs()
        # print(self._configurator.load_jobs())
        for row_index, job_data in enumerate(jobs):
            self._jobs_table.insertRow(row_index)
            for col_index, col_data in enumerate(job_data):
                item = QTableWidgetItem(col_data)
                self._jobs_table.setItem(row_index, col_index, item)

    def show_enable_proxy(self, current_server):
        """
        Function which handles whether the "Enable Proxy" button should be shown or not (based on the current server).
        :param current_server: `str` The current server URL.
        """
        try:
            if current_server == "http://localhost:8080" or "http://127.0.0.1:8080":
                self._enable_proxy_button.show()
            else:
                self._enable_proxy_button.hide()
        except:
            pass

    def set_new_current_server(self):
        """
        Function which sets the current server to the selected server from the server list.
        """
        current_index = self._server_list_view.selectionModel().currentIndex()

        if current_index.isValid():
            # Get the selected item from the model
            current_item = self._server_list.itemFromIndex(current_index)
            self._configurator.set_current_server(current_item.text())
            self.show_enable_proxy(current_item.text())
            self.update_current_server_label()
            self.update_jobs_table_for_new_server()

    def update_current_server_label(self):
        """
        Function which sets the current server label to the URL of the selected server from the server list.
        """
        link = "<a href=\"" + self._configurator.get_current_server().get_url() + "\" style='color: #81B622; text-decoration: none; font-size:22px;'>" + self._configurator.get_current_server().get_url() + "</a>"
        on_hover_link = "<a href=\"" + self._configurator.get_current_server().get_url() + "\" style='color: #81B622; text-decoration: underline; font-size:22px;'>" + self._configurator.get_current_server().get_url() + "</a>"
        self._current_server_label.setText(link)
        self._hover_filter.set_link(link)
        self._hover_filter.set_on_hover_link(on_hover_link)

    def find_index_by_url(self, url):
        """
        Function which finds the index of the selected server from the server list.
        :param url: `str` The URL of the selected server.
        :return: `int` The index of the selected server.
        """
        for row in range(self._server_list.rowCount()):
            item = self._server_list.item(row)
            if item.text() == url:
                return self._server_list.index(row, 0)
        return QtCore.QModelIndex()

    def show_create_job_view(self):
        """
        Function which shows the create job view.
        """
        self.create_job_form = CreateJobFormView(self._configurator.get_current_server())

    def show_connect_to_server_view(self):
        """
        Function which shows the connect to server view.
        """
        self.connect_to_server_form = ConnectToServerFormView(self._configurator)
        self.connect_to_server_form.finished_signal.connect(self.update_servers)

    def update_servers(self, status, msg):
        """
        Function which updates the servers list when a new server is added.
        :param status: `int` The status connecting to the server.
        :param msg: `str` The message to show.
        """
        if status == 1:
            self.update_servers_list()
            self.set_new_current_server()
