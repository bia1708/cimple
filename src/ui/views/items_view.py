from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from ui.components.list_view import ListView


class ItemsView(QWidget):
    def __init__(self, configurator):
        super().__init__()

        self._configurator = configurator

        self._server_list_label = QLabel("Server List")
        self._server_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._server_list_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._server_list_label.setWordWrap(True)
        self._server_list_view = ListView()
        # self._server_list.setModel(self._configurator.model())
        self._server_list = QtGui.QStandardItemModel()
        for server in self._configurator.get_all_servers():
            server_item = QtGui.QStandardItem(server.get_url())
            server_item.setEditable(True)
            self._server_list.appendRow(server_item)
        self._server_list_view.setModel(self._server_list)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(10)
        self.setLayout(self._layout)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._layout.addWidget(self._server_list_label)
        self._layout.addWidget(self._server_list_view)