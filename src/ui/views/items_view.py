from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QTableWidget, QTableWidgetItem
from ui.components.button import Button
from ui.components.table import Table
from ui.components.list_view import ListView


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
        for server in self._configurator.get_all_servers():
            server_item = QtGui.QStandardItem(server.get_url())
            server_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            server_item.setEditable(True)
            self._server_list.appendRow(server_item)
        self._server_list_view.setModel(self._server_list)

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

        self._current_server_label = QLabel(self._configurator.get_current_server().get_url())
        self._current_server_label.setStyleSheet("font-family: Inria Sans; font-size: 20px; text-align: center;")
        self._current_server_label.setWordWrap(True)
        self._current_server_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create a table to display the list of jobs for the current server
        self._jobs_table = Table()  # Rows and columns
        self._jobs_table.setHorizontalHeaderLabels(["My Jobs", "No. of Builds", "Status", "GitHub Status"])
        
        # Populate the table with dummy job data for demonstration
        jobs = [
            ["Job 1", "Running", "10:00 AM"],
            ["Job 2", "Completed", "11:30 AM"],
            ["Job 3", "Failed", "12:45 PM"],
        ]
        
        for row_index, job_data in enumerate(jobs):
            self._jobs_table.insertRow(row_index)
            for col_index, col_data in enumerate(job_data):
                item = QTableWidgetItem(col_data)
                self._jobs_table.setItem(row_index, col_index, item)

        self._add_job_button = Button("Create Job")
        self._add_job_button_layout = QHBoxLayout()
        self._add_job_button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._add_job_button_layout.addStretch()
        self._add_job_button_layout.addWidget(self._add_job_button)
        # self._add_job_button.setLayout(self._add_job_button_layout)

        self._right_column_layout.addWidget(self._current_server_label)
        self._right_column_layout.addWidget(self._jobs_table)
        self._right_column_layout.addWidget(self._add_job_button)
        self._right_column_layout.setSpacing(20)
        self._right_column.setLayout(self._right_column_layout)

        self._splitter.addWidget(self._left_column)
        self._splitter.addWidget(self._right_column)
        self._splitter.setSizes([300, 700])
        self._view_layout = QHBoxLayout()
        self._view_layout.addWidget(self._splitter)
        self.setLayout(self._view_layout)
