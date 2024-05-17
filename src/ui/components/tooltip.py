from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class CustomToolTip(QLabel):
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