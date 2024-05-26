"""
@Author: Bianca Popu (bia1708)
@Date: 17/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    """
    LineEdit Component Class for custom QLineEdits.
    """
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.setStyleSheet("QLineEdit { border: 2px solid gray; border-radius: 10px; padding: 2px; height: 30px }"
                           "QLineEdit:focus { border-color: #59981A; }")
