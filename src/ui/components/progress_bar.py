"""
@Author: Bianca Popu (bia1708)
@Date: 17/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
    """
    ProgressBar Component Class for custom progress bars.
    """
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)

        self.setMaximum(100)
        self.setMinimum(0)
        self.setGeometry(100, 100, 200, 100)

        self.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f0f0f0;
                color: black
                text-align: center;
            }
        
            QProgressBar::chunk {
                background-color: #81B622;
                border-radius: 5px;
            }
            """
)