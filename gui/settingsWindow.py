import sys, json, fileHandling
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                               QFileDialog, QMessageBox, QSplitter, QCheckBox, QComboBox)

class SettingsWindow(QWidget):
    def __init__(self, /):
        super().__init__()
        self.current_user = None
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.title = QLabel("Settings")
        self.cat1 = QLabel("Visual Settings")
        #self.dark_mode = QComboBox("Theme")
        # Adding Default, Dark Mode, Dark Blue, and Dark Purple
        self.cat2 = QLabel("Data Settings")
        self.delete_data_on_exit = QCheckBox("Delete Data When Exiting App")
        self.delete_data = QPushButton("Delete User Data")
        self.reset_settings = QPushButton("Reset Settings")
        self.close_settings = QPushButton("Save and Close")

        layout.addWidget(self.title)
        layout.addWidget(self.cat1)
        ##layout.addWidget(self.dark_mode)
        layout.addWidget(self.cat2)
        layout.addWidget(self.delete_data_on_exit)
        layout.addWidget(self.delete_data)
        layout.addWidget(self.reset_settings)
        layout.addWidget(self.close_settings)

        self.setLayout(layout)

        # going to add the connections and functions later ideally when ive thought of more settings to add in the first place

        # Connections

        self.delete_data.clicked.connect(self.delete_data_function)
        self.reset_settings.clicked.connect(self.reset_settings_function)
        self.close_settings.clicked.connect(self.close_settings_function)

    def delete_data_function(self):
        fileHandling.delete_folder(self.current_user)
        QMessageBox.information(self, "User Data Deleted.", "The user data has been deleted.")

    def set_current_user(self, username):
        self.current_user = username
        self.setWindowTitle(f"{self.current_user}'s Settings")
        settings = fileHandling.load_settings(self.current_user)

        settings = fileHandling.load_settings(self.current_user)
        if settings:
            self.delete_data_on_exit.setChecked(settings.get("delete_on_exit", False))

    def reset_settings_function(self):
        theme = "default"
        self.delete_data_on_exit = False
        ## save settings data here

    def close_settings_function(self):
        settings = {
            "delete_on_exit": self.delete_data_on_exit.isChecked()
        }
        fileHandling.save_settings(self.current_user, settings)
        self.close()
