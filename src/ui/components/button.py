from PySide6.QtWidgets import (
    QPushButton,
)


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: #59981A; color: #ECF87F; border-radius: 10px;")
        self.setFixedSize(self.sizeHint().width() + 20, self.sizeHint().height() + 20)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setStyleSheet("background-color: #3D550C; color: #ECF87F; border-radius: 10px;")

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setStyleSheet("background-color: #59981A; color: #ECF87F; border-radius: 10px;")
