from PySide6.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    def __init__(self, parent=None):
        super(MessageBox, self).__init__(parent)
        self.setWindowTitle('cimple')
        self.setIcon(QMessageBox.Icon.Information)

        self.setStyleSheet(
            """
            QMessageBox {
                background-color: #333333;
                color: white;
                font: bold 12pt;
            }

            QMessageBox QLabel {
                color: white;
            }

            QMessageBox QPushButton {
                background-color: #555555;
                color: white;
                border: 1px solid #888888;
                border-radius: 5px;
                padding: 5px;
            }

            QMessageBox QPushButton:hover {
                background-color: #666666;
            }

            QMessageBox QPushButton:pressed {
                background-color: #444444;
            }
            """
        )
