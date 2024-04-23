from PySide6.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView


class Table(QTableWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
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
