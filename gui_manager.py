import sys
import os

from PySide2.QtCore import Slot
from PySide2.QtGui import QKeySequence, QWindow
from PySide2.QtWidgets import QMainWindow, QAction, QApplication, QPushButton, QVBoxLayout, QWidget, QStackedLayout, \
    QLabel, QLineEdit, QFileDialog, QErrorMessage

from face_authentication import AppManager


class MessageWindow(QWindow):
    def __init__(self, message="Error", parent=None):
        QWindow.__init__(self, parent)

        self.layout = QVBoxLayout()

        self.message = QLabel(message)
        self.layout.addWidget(self.message)

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.close)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)


class ApplicationWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    @Slot()
    def back(self):
        self.parent().set_main_menu()


class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # TODO: finish this widget


class FaceLoadingWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__setup_ui()

    def __setup_ui(self):

        self.layout = QVBoxLayout()

        self.enter_name_label = QLabel("Enter user name:")
        self.layout.addWidget(self.enter_name_label)

        self.name_line_edit = QLineEdit()
        self.layout.addWidget(self.name_line_edit)

        self.id_label = QLabel("Enter user id (leave blank if the user is new)")
        self.layout.addWidget(self.id_label)

        self.id_line_edit = QLineEdit()
        self.layout.addWidget(self.id_line_edit)

        self.from_file_button = QPushButton("From file")
        self.from_file_button.clicked.connect(self.load_from_file)
        self.layout.addWidget(self.from_file_button)

        self.from_camera_button = QPushButton("From camera")
        self.from_camera_button.clicked.connect(self.load_from_camera)
        self.layout.addWidget(self.from_camera_button)

        self.layout.addStretch()

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    @Slot()
    def load_from_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open Image", os.getcwd(), "Image Files (*.png *.jpg *.bmp)")[0]
        user_name = self.name_line_edit.text()
        id_inp = self.id_line_edit.text()

        if not id_inp:
            id_ = app.get_next_face_id()
        else:
            id_ = int(id_inp)

        if file_name and user_name:
            app.load_from_file(file_name, id_, user_name)
            success_message = QErrorMessage(self)
            success_message.showMessage(f"Successfully loaded a new face of {user_name} (id {id_})")
            self.name_line_edit.clear()
            self.id_line_edit.clear()
        else:
            error_message = QErrorMessage(self)
            error_message.showMessage("File name or user name not provided")

    @Slot()
    def load_from_camera(self):
        user_name = self.name_line_edit.text()
        id_inp = self.id_line_edit.text()

        if not id_inp:
            id_ = app.get_next_face_id()
        else:
            id_ = int(id_inp)

        if user_name:
            app.load_from_camera(id_, user_name)
            success_message = QErrorMessage(self)
            success_message.showMessage(f"Successfully loaded a new face of {user_name} (id {id_})")
            self.name_line_edit.clear()
            self.id_line_edit.clear()
        else:
            error_message = QErrorMessage(self)
            error_message.showMessage("User name not provided")

    @Slot()
    def back(self):
        self.parent().set_main_menu()


class FaceAuthenticationWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.__setup_ui()

    def __setup_ui(self):
        self.layout = QVBoxLayout()

        self.start_button = QPushButton("Start (switch on the camera)")
        self.start_button.clicked.connect(self.authenticate)
        self.layout.addWidget(self.start_button)

        self.description = QLabel("Press ESC to quit authentication")
        self.layout.addWidget(self.description)

        self.layout.addStretch()

        self.back_button = QPushButton("Back to main menu")
        self.back_button.clicked.connect(self.back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    @Slot()
    def authenticate(self):
        app.authenticate()

    @Slot()
    def back(self):
        self.parent().set_main_menu()


class MainMenuWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__setup_ui()

    def __setup_ui(self):
        self.layout = QVBoxLayout()

        self.face_load_button = QPushButton("Load new face")
        self.face_load_button.clicked.connect(self.open_face_load_widget)
        self.layout.addWidget(self.face_load_button)

        self.face_auth_button = QPushButton("Start authentication")
        self.face_auth_button.clicked.connect(self.open_face_auth_widget)
        self.layout.addWidget(self.face_auth_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings_widget)
        self.layout.addWidget(self.settings_button)

        self.layout.addStretch()

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

    @Slot()
    def open_face_load_widget(self):
        self.parent().open_face_load_widget()

    @Slot()
    def open_face_auth_widget(self):
        self.parent().open_face_auth_widget()

    @Slot()
    def open_settings_widget(self):
        self.parent().open_settings_widget()

    @Slot()
    def quit(self):
        QApplication.quit()


class MainWindowCentralWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.__MAIN_MENU_WIDGET_NAME = 'main_menu'
        self.__SETTINGS_WIDGET_NAME = 'settings'
        self.__FACE_LOAD_WIDGET_NAME = 'face load'
        self.__FACE_AUTH_WIDGET_NAME = 'face auth'

        self.__setup_ui()

        self.widgets = {
            self.__MAIN_MENU_WIDGET_NAME: self.main_menu_widget,
            self.__SETTINGS_WIDGET_NAME: self.settings_widget,
            self.__FACE_LOAD_WIDGET_NAME: self.face_loading_widget,
            self.__FACE_AUTH_WIDGET_NAME: self.face_authentication_widget
        }

        # self.setLayout(self.stacked_layout)

    def __setup_ui(self):
        self.stacked_layout = QStackedLayout()

        self.main_menu_widget = MainMenuWidget(self)
        self.stacked_layout.addWidget(self.main_menu_widget)

        self.settings_widget = SettingsWidget(self)
        self.stacked_layout.addWidget(self.settings_widget)

        self.face_loading_widget = FaceLoadingWidget(self)
        self.stacked_layout.addWidget(self.face_loading_widget)

        self.face_authentication_widget = FaceAuthenticationWidget(self)
        self.stacked_layout.addWidget(self.face_authentication_widget)

        self.setLayout(self.stacked_layout)

    def set_current_widget(self, widget_name):
        self.stacked_layout.setCurrentWidget(self.widgets[widget_name])

    def set_main_menu(self):
        self.set_current_widget(self.__MAIN_MENU_WIDGET_NAME)

    def open_face_load_widget(self):
        self.set_current_widget(self.__FACE_LOAD_WIDGET_NAME)

    def open_settings_widget(self):
        self.set_current_widget(self.__SETTINGS_WIDGET_NAME)

    def open_face_auth_widget(self):
        self.set_current_widget(self.__FACE_AUTH_WIDGET_NAME)

    @Slot()
    def change_widget(self):
        self.stacked_layout.setCurrentWidget(self.settings_widget)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Face authentication app")

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)

        self.central_widget = MainWindowCentralWidget()
        self.setCentralWidget(self.central_widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == '__main__':
    ui_app = QApplication(sys.argv)
    app = AppManager()

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(ui_app.exec_())
