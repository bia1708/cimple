from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QTableWidgetItem, QSpacerItem, QSizePolicy
from ui.views.create_job_form import CreateJobFormView
from ui.components.button import Button
from ui.components.table import Table
from ui.components.list_view import ListView
from ui.components.link_event import LinkEvent
from ui.views.connect_to_server_form import ConnectToServerFormView


class ItemsView(QWidget):
    def __init__(self, configurator):
        super().__init__()

        self._configurator = configurator
        self._splitter = QSplitter(Qt.Horizontal)

        self._left_column = QWidget()
        self._server_list_label = QLabel("Server List")
        self._server_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._server_list_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._server_list_label.setWordWrap(True)

        self._server_list_view = ListView()
        self._server_list = QtGui.QStandardItemModel()
        self.update_servers_list()
        self._server_list_view.setModel(self._server_list)
        selection_model = self._server_list_view.selectionModel()
        selection_model.selectionChanged.connect(self.set_new_current_server)

        # Set the default selected item to be the last connected server
        default_index = self.find_index_by_url(self._configurator.get_current_server().get_url())  # Get the index of the first row
        selection_model.select(
            default_index, QtCore.QItemSelectionModel.Select
        )

        self._left_column_layout = QVBoxLayout()
        self._left_column_layout.setContentsMargins(0, 0, 0, 0)
        self._left_column_layout.setSpacing(10)
        self._left_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._left_column_layout.addWidget(self._server_list_label)
        self._left_column_layout.addWidget(self._server_list_view)
        self._left_column.setLayout(self._left_column_layout)

        self._right_column = QWidget()
        self._right_column_layout = QVBoxLayout()
        self._right_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        self._jobs_table.setHorizontalHeaderLabels(["My Jobs", "No. of Builds", "Status", "GitHub Status"])

        self.update_jobs_table()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_jobs_table)
        self.timer.start(2000)

        # Create job button + Connect to server button
        self._buttons_container = QWidget()
        self._buttons_container.setContentsMargins(0, 0, 0, 0)
        self._buttons_container_layout = QHBoxLayout()
        self._buttons_container.setLayout(self._buttons_container_layout)

        self._add_job_button = Button("Create Job")
        self._add_job_button.clicked.connect(self.show_create_job_view)

        self._connect_to_server_button = Button("Connect to Server")
        self._connect_to_server_button.clicked.connect(self.show_connect_to_server_view)

        self._buttons_container_layout.addWidget(self._connect_to_server_button)
        # self._configurator.get_all_servers()
        if self._configurator.get_server_by_url("http://127.0.0.1:8080") is not None and self._configurator.get_server_by_url("http://localhost:8080") is not None:
            self._fresh_install_button = Button("Fresh Install")
            self._fresh_install_button.clicked.connect(lambda: self.fresh_install_signal.emit(True))
            self._buttons_container_layout.addWidget(self._fresh_install_button)
        self._buttons_container_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        self._buttons_container_layout.addWidget(self._add_job_button)

        # Right column: Title label, table with jobs, create job button
        self._right_column_layout.addWidget(self._current_server_label)
        self._right_column_layout.addWidget(self._jobs_table)
        self._right_column_layout.addWidget(self._buttons_container)
        self._right_column_layout.setSpacing(20)
        self._right_column.setLayout(self._right_column_layout)

        self._splitter.addWidget(self._left_column)
        self._splitter.addWidget(self._right_column)
        self._splitter.setSizes([300, 700])
        self._view_layout = QHBoxLayout()
        self._view_layout.addWidget(self._splitter)
        self.setLayout(self._view_layout)
    
    fresh_install_signal = Signal(bool)

    def update_servers_list(self):
        self._server_list.clear()
        for server in self._configurator.get_all_servers():
            server_item = QtGui.QStandardItem(server.get_url())
            server_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            server_item.setEditable(False)
            self._server_list.appendRow(server_item)

    def update_jobs_table(self):
        # Get current contents first
        current_rows = []
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
        jobs = self._configurator.load_jobs()
        for row_index, job_data in enumerate(jobs):
            if job_data not in current_rows:
                job_titles = [x[0] for x in current_rows]
                if job_data[0] not in job_titles:
                    self._jobs_table.insertRow(row_index)
                for col_index, col_data in enumerate(job_data):
                    item = QTableWidgetItem(col_data)
                    self._jobs_table.setItem(row_index, col_index, item)

    def set_new_current_server(self):
        current_index = self._server_list_view.selectionModel().currentIndex()

        if current_index.isValid():
            # Get the selected item from the model
            current_item = self._server_list.itemFromIndex(current_index)
            self._configurator.set_current_server(current_item.text())
            self.update_current_server_label()

    def update_current_server_label(self):
        link = "<a href=\"" + self._configurator.get_current_server().get_url() + "\" style='color: #81B622; text-decoration: none; font-size:22px;'>" + self._configurator.get_current_server().get_url() + "</a>"
        on_hover_link = "<a href=\"" + self._configurator.get_current_server().get_url() + "\" style='color: #81B622; text-decoration: underline; font-size:22px;'>" + self._configurator.get_current_server().get_url() + "</a>"
        self._current_server_label.setText(link)
        self._hover_filter.set_link(link)
        self._hover_filter.set_on_hover_link(on_hover_link)

    def find_index_by_url(self, url):
        for row in range(self._server_list.rowCount()):
            item = self._server_list.item(row)
            if item.text() == url:
                return self._server_list.index(row, 0)
        return QtCore.QModelIndex()

    def show_create_job_view(self):
        self.create_job_form = CreateJobFormView(self._configurator.get_current_server())
        # create_job_form.show()
        # job_window = QMainWindow()
        # job_window.setCentralWidget(create_job_form)
        # job_window.show()

    def show_connect_to_server_view(self):
        self.connect_to_server_form = ConnectToServerFormView(self._configurator)
        self.connect_to_server_form.finished_signal.connect(self.update_servers)

    def update_servers(self, status, msg):
        if status == 1:
            self.update_servers_list()
            self.set_new_current_server()
