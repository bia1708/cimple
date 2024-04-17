from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QLabel

from src.ui.components.progress_bar import ProgressBar


class InstallProgressView(QWidget):
    def __init__(self):
        super().__init__()
        self._heading_label = QLabel("Configuring Jenkins Setup")
        self._heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._heading_label.setStyleSheet('font-family: Inria Sans; font-size: 22px; text-align: center;')
        self._heading_label.setWordWrap(True)

        self._subheading_label = QLabel("This will take a while ...")
        self._subheading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subheading_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        self._subheading_label.setWordWrap(True)

        self.progressBar = ProgressBar()
        self.progressBar.setValue(50)

        layout = QVBoxLayout()
        layout.addWidget(self._heading_label)
        layout.addWidget(self._subheading_label)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)
