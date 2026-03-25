import sys, json
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                               QFileDialog, QMessageBox, QSplitter, QCheckBox, QComboBox)
import fileHandling
from gui.loginWIndow import LoginWindow

class SettingsWindow(QWidget):
    def __init__(self, /):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.title = QLabel("Settings")
        self.cat1 = QLabel("Visual Settings")
        self.dark_mode = QComboBox("Theme")
        ## Adding Default, Dark Mode, Dark Blue, and Dark Purple
        self.cat2 = QLabel("Data Settings")
        self.delete_data_on_exit = QCheckBox("Delete Data When Exiting App")
        self.delete_data = QPushButton("Delete User Data")
        self.reset_settings = QPushButton("Reset Settings")
        self.close_settings = QPushButton("Save and Close")

        layout.addWidget(self.title)
        layout.addWidget(self.cat1)
        layout.addWidget(self.dark_mode)
        layout.addWidget(self.cat2)
        layout.addWidget(self.delete_data_on_exit)
        layout.addWidget(self.delete_data)
        layout.addWidget(self.reset_settings)
        layout.addWidget(self.close_settings)

        self.setLayout(layout)

        # going to add the connections and functions later ideally when ive thought of more settings to add in the first place
