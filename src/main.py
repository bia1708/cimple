"""
@Author: Bianca Popu (bia1708)
@Date: 6/03/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication()
    app.setApplicationName('cimple')

    window = MainWindow()

    app.setWindowIcon(QIcon("src/ui/resources/cimple.ico"))

    app.exec()
