"""
@Author: Bianca Popu (bia1708)
@Date: 16/04/2024
@Links: https://github.com/bia1708/cimple.git
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QHBoxLayout, QLabel
)

from src.service.configurator import Configurator
from src.ui.components.button import Button
from src.ui.views.connect_to_server_form import ConnectToServerFormView
from src.ui.views.install_form import InstallFormView
from src.ui.views.install_progress import InstallProgressView
from src.ui.views.items_view import ItemsView


class MainWindow(QMainWindow):
    """
    Main Window View Class. Main entry point of the GUI and controller for views.
    :ivar __configurator: `Configurator` instance
    """
    def __init__(self):
        super().__init__()
        self.__configurator = Configurator()
        self.setWindowTitle('cimple')
        self.resize(800, 500)
        self.setWindowIcon(QIcon("src/ui/resources/icon.png"))
        if self.__configurator.get_number_of_servers() == 0:
            self.startup_ui()
        else:
            self.switch_to_list_view()
        self.show()

    def switch_to_install_form(self):
        """
        Function which switches to the install form view.
        """
        install_form_view = InstallFormView()
        install_form_view.form_signal.connect(self.switch_to_install_progress)
        self.setCentralWidget(install_form_view)

    def switch_to_connect_form(self):
        """
        Function which switches to the connect form view.
        """
        self.connect_to_server_view = ConnectToServerFormView(self.__configurator)
        self.connect_to_server_view.finished_signal.connect(self.finish_connect)

    def finish_connect(self, status, msg):
        """
        Function which switches to the list view after successfully connecting to a server.
        :param status: `int` status code
        :param msg: `str` message
        """
        if status == 1:
            self.switch_to_list_view()

    def switch_to_install_progress(self, username, password, proxy):
        """
        Function which switches to the install progress view.
        :param username: `str` Jenkins username
        :param password: `str` Jenkins password
        :param proxy: `boolean` True if "enable proxy" is enabled
        """
        install_progress_view = InstallProgressView(self.__configurator, username, password, proxy)
        self.setCentralWidget(install_progress_view)
        install_progress_view.error_signal.connect(self.install_error_comeback)
        install_progress_view.change_view_signal.connect(lambda: self.switch_to_list_view())

    def switch_to_list_view(self):
        """
        Function which switches to the list view after successfully performing a fresh install.
        """
        self.list_view = ItemsView(self.__configurator)
        self.list_view.fresh_install_signal.connect(self.switch_to_install_form)
        self.setCentralWidget(self.list_view)

    def install_error_comeback(self):
        """
        Function which switches to the welcome view in case of errors.
        """
        if len(self.__configurator.get_all_servers()) > 0 and self.__configurator.get_server_by_url("http://127.0.0.1:8080") is not None \
            and self.__configurator.get_server_by_url("http://localhost:8080") is not None:
            self.switch_to_list_view()
        else:
            self.startup_ui()

    def startup_ui(self):
        """
        Function which constructs the welcome view.
        """
        label_widget = QWidget(self)
        self.setCentralWidget(label_widget)

        layout = QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        label_widget.setLayout(layout)  # Assign the layout to the widget

        heading_label = QLabel(self)
        heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading_label.setStyleSheet('font-family: Inria Sans; font-size: 22px; text-align: center;')
        heading_label.setWordWrap(True)
        heading_label.setText("Welcome to cimple!")
        label_widget.layout().addWidget(heading_label)

        subheading_label = QLabel(self)
        subheading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subheading_label.setStyleSheet('font-family: Inria Sans; font-size: 18px; text-align: center;')
        subheading_label.setWordWrap(True)
        subheading_label.setText("If you don't have Jenkins setup on your system, choose fresh installation. Or, you"
                                 "can connect to an existing instance and start automating your workflows instantly!")
        label_widget.layout().addWidget(subheading_label)

        buttons_widget = QWidget(self)
        buttons_widget.setLayout(QHBoxLayout())
        btn1 = Button('Connect to Existing Instance', buttons_widget)
        btn2 = Button('Fresh Install', buttons_widget)

        btn1.pressed.connect(self.switch_to_connect_form)
        btn2.pressed.connect(self.switch_to_install_form)

        buttons_widget.layout().addWidget(btn1)
        buttons_widget.layout().addWidget(btn2)
        label_widget.layout().addWidget(buttons_widget)

        return label_widget

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Function which closes the configurator (and implicitly the repository).
        :param event: `QCloseEvent` event which closes the window.
        """
        self.__configurator.close()
        return super().closeEvent(event)
