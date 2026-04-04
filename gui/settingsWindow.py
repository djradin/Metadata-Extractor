from framework import fileHandling
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                               QMessageBox, QCheckBox, QComboBox)

class SettingsWindow(QWidget):

    theme_changed = Signal(str)
    files_changed = Signal()

    def __init__(self, /):
        super().__init__()

        self.current_user = None
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()

        self.title = QLabel("Settings")
        self.cat1 = QLabel("Visual Settings")
        self.big_text = QCheckBox("Big Text")
        self.bold_text = QCheckBox("Bold Text")
        self.themes_label = QLabel("Application Theme")
        self.themes = QComboBox()
        self.themes.addItems(["Default", "Dark", "Dark Blue", "Dark Purple", "Eye Sore"])
        self.cat2 = QLabel("Data Settings")
        self.delete_data_on_exit = QCheckBox("Delete Data When Exiting Session")
        self.delete_data = QPushButton("Delete User Data")
        self.reset_settings = QPushButton("Reset Settings")
        self.close_settings = QPushButton("Save and Close")

        layout.addWidget(self.title)
        layout.addWidget(self.cat1)
        layout.addWidget(self.big_text)
        layout.addWidget(self.bold_text)
        layout.addWidget(self.themes_label)
        layout.addWidget(self.themes)
        layout.addWidget(self.cat2)
        layout.addWidget(self.delete_data_on_exit)
        layout.addWidget(self.delete_data)
        layout.addWidget(self.reset_settings)
        layout.addWidget(self.close_settings)

        self.setLayout(layout)

        # Connections

        self.delete_data.clicked.connect(self.delete_data_function)
        self.reset_settings.clicked.connect(self.reset_settings_function)
        self.close_settings.clicked.connect(self.close_settings_function)
        self.themes.currentTextChanged.connect(self.apply_theme)

    def delete_data_function(self):
        fileHandling.delete_folder(self.current_user)
        self.files_changed.emit()
        QMessageBox.information(self, "User Data Deleted.", "The user data has been deleted.")

    def set_current_user(self, username):
        self.current_user = username
        self.setWindowTitle(f"{self.current_user}'s Settings")
        settings = fileHandling.load_settings(self.current_user)
        if settings:
            self.delete_data_on_exit.setChecked(settings.get("delete_on_exit", False))

            theme = settings.get("theme", "Default")
            self.themes.setCurrentText(theme)
            self.apply_theme(theme)

    def reset_settings_function(self):
        self.delete_data_on_exit.setChecked(False)
        self.themes.setCurrentText("Default")
        self.apply_theme("Default")

        settings = {
            "delete_on_exit": False,
            "theme": "Default"
        }
        fileHandling.save_settings(self.current_user, settings)

    def close_settings_function(self):
        settings = {
            "delete_on_exit": self.delete_data_on_exit.isChecked(),
            "theme": self.themes.currentText()
        }
        fileHandling.save_settings(self.current_user, settings)
        theme = self.themes.currentText()
        self.theme_changed.emit(theme)
        self.close()

    def apply_theme(self, theme):
        if theme == "Dark":
            self.setStyleSheet("""
                        QWidget {
                            background-color: #2a2a2a;
                            color: white;
                        }
                        QPushButton {
                            background-color: #444;
                            color: white;
                            border: none;
                            padding: 5px;
                        }
                        QComboBox {
                            background-color: #444;
                            color: white;
                            border: none;
                            padding: 5px;
                        }
                    """)
        elif theme == "Dark Blue":
            self.setStyleSheet("""
                        QWidget {
                            background-color: #0d1b2a;
                            color: white;
                        }
                        QPushButton {
                            background-color: #1a2640;
                            color: white;
                            border: none;
                            padding: 5px;
                        }
                        QComboBox {
                            background-color: #1a2640;
                            color: white;
                            border: none;
                            padding: 5px;
                        }
                    """)
        elif theme == "Dark Purple":
            self.setStyleSheet("""
                        QWidget {
                            background-color: #2b2d42;
                            color: white;
                        }
                        QPushButton {
                            background-color: #5a5f9e;
                            color: white; 
                            border: none;
                            padding: 5px;
                        }
                        QComboBox {
                            background-color: #5a5f9e;
                            color: white; 
                            border: none;
                            padding: 5px;
                        }
                    """)
        elif theme == "Eye Sore":
            self.setStyleSheet("""
                        QWidget {
                            background-color: #fafefa;
                            color: #0000ff;
                        }
                        QPushButton {
                            background-color: #ffaa00;
                            color: #0000ff; 
                            border: none;
                            padding: 1px;
                        }
                        QComboBox {
                            background-color: #ad72fe;
                            color: #00ff00; 
                            border: none;
                            padding: 2px;
                        }
                    """)
        else:
            self.setStyleSheet("")