"""
@Author: Bianca Popu (bia1708)
@Date: 27/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtCore import QObject, QEvent

class LinkEvent(QObject):
    """
    Custom Event Class for custom link events (update text on hover, click on link)
    """
    def __init__(self, link=None, on_hover_link=None, parent=None):
        super().__init__(parent)
        self._link = link
        self._on_hover_link = on_hover_link

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            # Change style when hovering
            obj.setText(self._on_hover_link)
        elif event.type() == QEvent.Leave:
            # Revert style when leaving
            obj.setText(self._link)
        return False

    def set_link(self, link):
        self._link = link

    def set_on_hover_link(self, on_hover_link):
        self._on_hover_link = on_hover_link
