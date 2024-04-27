import sys

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QHBoxLayout, QLabel
)

from service.configurator import Configurator
from ui.components.button import Button
from ui.views.install_form import InstallFormView
from ui.views.install_progress import InstallProgressView
from ui.views.items_view import ItemsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__configurator = Configurator()
        # self.__configurator.add_jenkins_instance("mock-url", "mock-username", "mock-token", "mock-jnlp")
        # self._main_window = QMainWindow()
        self.setWindowTitle('cimple')
        self.resize(800, 500)
        self.setWindowIcon(QIcon("ui/resources/icon.png"))
        # TODO: Maybe transitions?
        # self._main_layout = QVBoxLayout()
        # self._stacked_widget = QStackedWidget()
        # self._main_layout.addWidget(self._stacked_widget)
        if self.__configurator.get_number_of_servers() == 0:
            self.startup_ui()
        else:
            self.switch_to_list_view()
        self.show()

    def switch_to_install_form(self):
        install_form_view = InstallFormView()
        install_form_view.form_signal.connect(self.switch_to_install_progress)
        self.setCentralWidget(install_form_view)

        # TODO: Maybe transitions??
        # self._stacked_widget.addWidget(install_form_view)
        # self.animate_transition(install_form_view)
        # self._stacked_widget.setCurrentWidget(install_form_view)

    def switch_to_install_progress(self, username, password, proxy):
        print(username, password, proxy)
        install_progress_view = InstallProgressView(self.__configurator, username, password, proxy)
        self.setCentralWidget(install_progress_view)
        install_progress_view.error_signal.connect(lambda: self.startup_ui())
        install_progress_view.change_view_signal.connect(lambda: self.switch_to_list_view())

    def switch_to_list_view(self):
        list_view = ItemsView(self.__configurator)
        self.setCentralWidget(list_view)

    def startup_ui(self):
        label_widget = QWidget(self)
        self.setCentralWidget(label_widget)

        # TODO: Fix too much spacing here
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
        subheading_label.setText("If you don't have Jenkins setup on your system, choose fresh installation." + \
                                 " Or, you can connect to an existing instance and start automating your workflows instantly!")
        label_widget.layout().addWidget(subheading_label)

        buttons_widget = QWidget(self)
        # window.setCentralWidget(buttons_widget)
        buttons_widget.setLayout(QHBoxLayout())
        btn1 = Button('Connect to Existing Instance', buttons_widget)
        btn2 = Button('Fresh Install', buttons_widget)

        btn2.pressed.connect(self.switch_to_install_form)

        buttons_widget.layout().addWidget(btn1)
        buttons_widget.layout().addWidget(btn2)
        label_widget.layout().addWidget(buttons_widget)

        return label_widget

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__configurator.close()
        return super().closeEvent(event)

    # def close(self, event):
    #     print("HERE")
    #     print(self.__configurator.get_current_server())
    #     self.__configurator.close()
    #     event.accept()
    #     return super().closeEvent(event)

    # def animate_transition(self, widget):
    #     # Create a property animation to animate the opacity of the widget
    #     animation = QPropertyAnimation(widget, b"opacity")
    #     animation.setDuration(500)  # Set the duration of the animation in milliseconds
    #     animation.setStartValue(0.0)  # Set the start value of the opacity
    #     animation.setEndValue(1.0)  # Set the end value of the opacity
    #     animation.setEasingCurve(QEasingCurve())  # Set the easing curve for smooth animation
    #     animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)  # Start the animation and delete it when stopped
