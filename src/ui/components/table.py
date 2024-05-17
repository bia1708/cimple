from PySide6.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor

from ui.components.tooltip import CustomToolTip


class Table(QTableWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.custom_tooltip = CustomToolTip(self)
        self.custom_tooltip.hide()

        self.setColumnCount(4)
        self.setRowCount(0)

        self.setWordWrap(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()

        self.setStyleSheet(
            """
            QTableWidget {
                background-color: #2E2E2E;
                color: white;
                border: none;
                padding:5px;
            }

            QTableWidget QHeaderView::section {
                color: white;
                border:none;
                border-bottom: 1px solid #CCCCCC;
                padding: 5px;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 10px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background-color: #81B622;
                color: black;
                border:none;
            }
            
            QTableWidget::item:hover {
                background-color: rgba(129, 182, 34, 150);
                color: black;
            }
            """
        )

    def mouseMoveEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item.column() == 2:  # Column where you want the custom tooltip
            tooltip_text = f"Click <a href='{item.data(Qt.ItemDataRole.BackgroundRole)}console'>here</a> to view the full status."
            global_pos = self.viewport().mapToGlobal(event.pos())
            pos = QPoint(global_pos.x(), global_pos.y() - self.custom_tooltip.height() - 10)  # Adjust position as needed
            self.custom_tooltip.show_tooltip(tooltip_text, pos)
        else:
            self.custom_tooltip.hide()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):  # Check if mouse is not over the table widget
            self.custom_tooltip.hide()
        super().leaveEvent(event)
