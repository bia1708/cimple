"""
@Author: Bianca Popu (bia1708)
@Date: 17/05/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class CustomToolTip(QLabel):
    """
    CustomToolTip Component Class for custom tool tips.
    """
    def __init__(self, parent=None):
        super().__init__(parent, Qt.ToolTip)
        self.setWindowFlags(Qt.ToolTip)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setWordWrap(True)
        self.setTextFormat(Qt.RichText)
        self.setOpenExternalLinks(True)

    def show_tooltip(self, text, pos):
        self.setText(text)
        self.adjustSize()
        # self.setFixedSize(100, 30)
        self.move(pos)
        self.show()