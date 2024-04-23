from PySide6.QtWidgets import QListView
from PySide6.QtCore import QSize



class ListView(QListView):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        
        self.setMouseTracking(True)

        self.setStyleSheet(
            """
            QListView {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #444444;
                font-size: 16px;
            }

            QListView {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #444444;
                font-size: 16px;
            }

            QListView::item {
                height: 25px;
                padding: 5px;
                background-color: #2E2E2E;
            }

            QListView::item:selected {
                padding: 5px;
                color: black;
                background-color: #81B622;
            }

            QListView::item:hover {
                padding: 5px;
                border: 0.5px solid #81B622;
                background-color: #2E2E2E;
                color: #ECF87F;
            }

            QListView::item:focus {
                outline: none;
            }

            QListView QScrollBar:vertical {
                background: #2E2E2E;
                width: 15px;
            }

            QListView QScrollBar::handle:vertical {
                background: #555555;
                border-radius: 7px;
            }

            QListView QScrollBar::add-page, QListView QScrollBar::sub-page {
                background: none;
            }
            """)