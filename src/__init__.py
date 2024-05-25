from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    app = QApplication()
    app.setApplicationName('cimple')

    window = MainWindow()

    app.setWindowIcon(QIcon("src/ui/resources/cimple.ico"))

    app.exec()
