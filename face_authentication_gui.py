import sys
import os

from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import QMainWindow, QAction, QApplication, QPushButton, QVBoxLayout, QWidget, QStackedLayout, \
    QLabel, QLineEdit, QFileDialog, QErrorMessage, QHBoxLayout, QSlider

from face_authentication import AppManager, EmptyImageError, FaceNotFoundError


class SettingsWidget(QWidget):
    """
    Widget that provides GUI in Settings page.
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__setup_ui()
        self.__cur_dir_name = app.faces_dir

    def __setup_ui(self):
        self.layout = QVBoxLayout()

        self.faces_directory_choose_layout = QHBoxLayout()
        self.faces_directory_choose_description = QLabel(f"Faces saves directory: {app.faces_dir}")
        self.faces_directory_choose_layout.addWidget(self.faces_directory_choose_description)

        self.faces_directory_choose_button = QPushButton("Change...")
        self.faces_directory_choose_button.clicked.connect(self.set_faces_directory)
        self.faces_directory_choose_layout.addWidget(self.faces_directory_choose_button)

        self.layout.addLayout(self.faces_directory_choose_layout)

        self.confidence_threshold_layout = QHBoxLayout()
        self.confidence_threshold_description = QLabel(f"Confidence distance threshold: {app.confidence_threshold}")
        self.confidence_threshold_layout.addWidget(self.confidence_threshold_description)

        self.confidence_threshold_slider = QSlider()
        self.confidence_threshold_slider.setOrientation(Qt.Horizontal)
        self.confidence_threshold_slider.setMinimum(0)
        self.confidence_threshold_slider.setMaximum(100)
        self.confidence_threshold_slider.setSingleStep(2)
        self.confidence_threshold_slider.setValue(app.confidence_threshold)
        self.confidence_threshold_slider.valueChanged.connect(self.set_confidence_threshold)
        self.confidence_threshold_layout.addWidget(self.confidence_threshold_slider)

        self.layout.addLayout(self.confidence_threshold_layout)

        self.camera_img_count_layout = QHBoxLayout()
        self.camera_img_count_description = QLabel(f"Camera shots while loading a face: {app.camera_image_count}")
        self.camera_img_count_layout.addWidget(self.camera_img_count_description)

        self.camera_img_count_slider = QSlider()
        self.camera_img_count_slider.setOrientation(Qt.Horizontal)
        self.camera_img_count_slider.setMinimum(1)
        self.camera_img_count_slider.setMaximum(30)
        self.camera_img_count_slider.setSingleStep(1)
        self.camera_img_count_slider.setValue(app.camera_image_count)
        self.camera_img_count_slider.valueChanged.connect(self.set_camera_img_count)
        self.camera_img_count_layout.addWidget(self.camera_img_count_slider)

        self.layout.addLayout(self.camera_img_count_layout)

        self.fps_layout = QHBoxLayout()
        self.fps_label = QLabel(f"FPS: {app.fps}")
        self.fps_layout.addWidget(self.fps_label)

        self.fps_slider = QSlider()
        self.fps_slider.setOrientation(Qt.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(30)
        self.fps_slider.setSingleStep(1)
        self.fps_slider.setValue(app.fps)
        self.fps_slider.valueChanged.connect(self.set_fps)
        self.fps_layout.addWidget(self.fps_slider)

        self.layout.addLayout(self.fps_layout)

        self.scale_factor_layout = QHBoxLayout()
        self.scale_factor_label = QLabel("Scale factor")
        self.scale_factor_layout.addWidget(self.scale_factor_label)

        self.scale_factor_line_edit = QLineEdit()
        self.scale_factor_line_edit.setText(str(app.scale_factor))
        self.scale_factor_layout.addWidget(self.scale_factor_line_edit)

        self.layout.addLayout(self.scale_factor_layout)

        self.min_neighbors_layout = QHBoxLayout()
        self.min_neighbors_label = QLabel(f"Min neighbors: {app.min_neighbors}")
        self.min_neighbors_layout.addWidget(self.min_neighbors_label)

        self.min_neighbors_slider = QSlider()
        self.min_neighbors_slider.setOrientation(Qt.Horizontal)
        self.min_neighbors_slider.setMinimum(1)
        self.min_neighbors_slider.setMaximum(10)
        self.min_neighbors_slider.setSingleStep(1)
        self.min_neighbors_slider.setValue(app.min_neighbors)
        self.min_neighbors_slider.valueChanged.connect(self.set_min_neighbors)
        self.min_neighbors_layout.addWidget(self.min_neighbors_slider)

        self.layout.addLayout(self.min_neighbors_layout)

        self.min_size_layout = QHBoxLayout()
        self.min_size_label = QLabel("Min size")
        self.min_size_layout.addWidget(self.min_size_label)

        x, y = app.min_size

        self.min_size_x_y_layout = QVBoxLayout()
        self.min_size_x_layout = QHBoxLayout()
        self.min_size_x_label = QLabel(f"Width: {x}")
        self.min_size_x_layout.addWidget(self.min_size_x_label)

        self.min_size_x_slider = QSlider()
        self.min_size_x_slider.setOrientation(Qt.Horizontal)
        self.min_size_x_slider.setMinimum(1)
        self.min_size_x_slider.setMaximum(24)
        self.min_size_x_slider.setSingleStep(1)
        self.min_size_x_slider.setValue(x)
        self.min_size_x_slider.valueChanged.connect(self.set_min_size_x)
        self.min_size_x_layout.addWidget(self.min_size_x_slider)

        self.min_size_y_layout = QHBoxLayout()
        self.min_size_y_label = QLabel(f"Height: {y}")
        self.min_size_y_layout.addWidget(self.min_size_y_label)

        self.min_size_y_slider = QSlider()
        self.min_size_y_slider.setOrientation(Qt.Horizontal)
        self.min_size_y_slider.setMinimum(1)
        self.min_size_y_slider.setMaximum(24)
        self.min_size_y_slider.setValue(y)
        self.min_size_y_slider.valueChanged.connect(self.set_min_size_y)
        self.min_size_y_layout.addWidget(self.min_size_y_slider)

        self.min_size_x_y_layout.addLayout(self.min_size_x_layout)
        self.min_size_x_y_layout.addLayout(self.min_size_y_layout)

        self.min_size_layout.addLayout(self.min_size_x_y_layout)
        self.layout.addLayout(self.min_size_layout)

        self.layout.addStretch()

        self.save_settings_button = QPushButton("Save")
        self.save_settings_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_settings_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    @Slot()
    def set_min_size_x(self):
        self.min_size_x_label.setText(f"Width: {self.min_size_x_slider.value()}")

    @Slot()
    def set_min_size_y(self):
        self.min_size_y_label.setText(f"Height: {self.min_size_y_slider.value()}")


    @Slot()
    def set_min_neighbors(self):
        self.min_neighbors_label.setText(f"Min neighbors: {self.min_neighbors_slider.value()}")

    @Slot()
    def set_fps(self):
        self.fps_label.setText(f"FPS: {self.fps_slider.value()}")

    @Slot()
    def set_camera_img_count(self):
        self.camera_img_count_description.setText(
            f"Camera shots while loading a face: {self.camera_img_count_slider.value()}")

    @Slot()
    def set_faces_directory(self):
        self.__cur_dir_name = QFileDialog.getExistingDirectory(
            self, "Open Directory", "", options=QFileDialog.ShowDirsOnly)
        self.faces_directory_choose_description.setText(f"Faces saves directory: {self.__cur_dir_name}")

    @Slot()
    def back(self):
        self.reset_faces_directory()
        self.reset_confidence_threshold()
        self.reset_camera_img_count()
        self.reset_min_neighbors()

        self.parent().set_main_menu()

    def reset_min_neighbors(self):
        self.min_neighbors_slider.setValue(app.min_neighbors)
        self.min_neighbors_label.setText(f"Min neighbors: {app.min_neighbors}")

    @Slot()
    def save_settings(self):
        try:
            app.set_faces_dir(self.__cur_dir_name)
            app.set_confidence_threshold(self.confidence_threshold_slider.value())
            app.set_camera_image_count(self.camera_img_count_slider.value())
            app.set_fps(self.fps_slider.value())
            app.set_scale_factor(float(self.scale_factor_line_edit.text()))
            app.set_min_neighbors(self.min_neighbors_slider.value())
            app.set_min_size(self.min_size_x_slider.value(), self.min_size_y_slider.value())
        except (NotADirectoryError, ValueError) as e:
            error_message = QErrorMessage(self)
            error_message.showMessage(str(e))
        except Exception as e:
            error_message = QErrorMessage(self)
            error_message.showMessage(f"Unknown error: {e}")
        error_message = QErrorMessage(self)
        error_message.showMessage("Saved successfully")

    @Slot()
    def set_confidence_threshold(self):
        self.confidence_threshold_description.setText(
            f"Confidence distance threshold: {self.confidence_threshold_slider.value()}")

    def reset_confidence_threshold(self):
        self.confidence_threshold_description.setText(f"Confidence distance threshold: {app.confidence_threshold}")
        self.confidence_threshold_slider.setValue(app.confidence_threshold)

    def reset_faces_directory(self):
        self.__cur_dir_name = app.faces_dir
        self.faces_directory_choose_description.setText(f"Faces directory: {self.__cur_dir_name}")

    def reset_camera_img_count(self):
        self.camera_img_count_description.setText(f"Camera shots while loading a face: {app.camera_image_count}")
        self.camera_img_count_slider.setValue(app.camera_image_count)


class FaceLoadingWidget(QWidget):
    """
    Widget that provides GUI in Face loading page.
    """
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
            try:
                app.load_from_file(file_name, id_, user_name)
                success_message = QErrorMessage(self)
                success_message.showMessage(f"Successfully loaded a new face of {user_name} (id {id_})")
                self.name_line_edit.clear()
                self.id_line_edit.clear()
            except (EmptyImageError, FaceNotFoundError) as e:
                error_message = QErrorMessage(self)
                error_message.showMessage(str(e))
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
    """
    Widget that provides GUI in Face authentication page.
    """
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

        self.stop_button = QPushButton("Stop (switch off the camera)")
        self.stop_button.clicked.connect(self.stop_authentication)
        self.stop_button.setEnabled(False)  # disable the button until the camera is switched on
        self.layout.addWidget(self.stop_button)

        self.layout.addStretch()

        self.back_button = QPushButton("Back to main menu")
        self.back_button.clicked.connect(self.back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    @Slot()
    def stop_authentication(self):
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        app.camera_off()

    @Slot()
    def authenticate(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        app.authenticate()

    @Slot()
    def back(self):
        self.parent().set_main_menu()


class MainMenuWidget(QWidget):
    """
    Widget that provides GUI in Main menu.
    """
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
    """
    Container for all widgets of pages in the application.
    """
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

    def set_current_widget(self, widget_name: str):
        """
        Choose which widget (page) to display
        :param widget_name: name of the widget to switch
        """
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
    """
    Main window of the application.
    """
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
