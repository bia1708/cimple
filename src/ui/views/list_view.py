from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout


class ListView(QWidget):
    def __init__(self, configurator):
        super().__init__()

        self._configurator = configurator
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._layout.addWidget(self._configurator)