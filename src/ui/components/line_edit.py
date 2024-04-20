from PySide6.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.setStyleSheet("QLineEdit { border: 2px solid gray; border-radius: 10px; padding: 2px; height: 30px }"
                           "QLineEdit:focus { border-color: #59981A; }")
