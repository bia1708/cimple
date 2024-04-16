import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem, QHBoxLayout, QLabel
)

from src.service.configurator import Configurator
from src.ui.components.button import Button


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__configurator = Configurator()
        self._main_window = self.startup_ui()
        self._main_window.show()

    def startup_ui(self):
        window = QMainWindow()
        window.setWindowTitle('cimple')
        window.resize(600, 400)
        window.setWindowIcon(QIcon('components/icon.png'))

        label_widget = QWidget(window)
        window.setCentralWidget(label_widget)

        # TODO: Fix too much spacing here
        layout = QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        label_widget.setLayout(layout)  # Assign the layout to the widget
        # label_widget.setLayout(QVBoxLayout())

        heading_label = QLabel(window)
        heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading_label.setStyleSheet('font-family: Inria Sans; font-size: 22px; text-align: center;')
        heading_label.setWordWrap(True)
        heading_label.setText("Welcome to cimple")
        label_widget.layout().addWidget(heading_label)

        subheading_label = QLabel(window)
        subheading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subheading_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        subheading_label.setWordWrap(True)
        subheading_label.setText("If you don’t have Jenkins setup on your system, choose fresh installation." + \
                                 "Or, you can connect to an existing instance and start automating your workflows instantly!")
        label_widget.layout().addWidget(subheading_label)

        buttons_widget = QWidget(window)
        # window.setCentralWidget(buttons_widget)
        buttons_widget.setLayout(QHBoxLayout())
        btn1 = Button('Connect to Existing Instance', buttons_widget)
        btn2 = Button('Fresh Install', buttons_widget)

        btn2.pressed.connect(self.__configurator.mock_method)

        buttons_widget.layout().addWidget(btn1)
        buttons_widget.layout().addWidget(btn2)
        label_widget.layout().addWidget(buttons_widget)
        return window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(app.exec())
