from framework import fileHandling
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                               QMessageBox, QCheckBox, QComboBox)
from PySide6.QtGui import QFont
from gui.changePasswordWindow import ChangePasswordWindow

class SettingsWindow(QWidget):

    theme_changed = Signal(str)
    files_changed = Signal()
    text_changed = Signal(bool, bool)

    def __init__(self, /):
        super().__init__()

        self.current_user = None
        self.pass_window = ChangePasswordWindow(self.current_user)
        self.setFixedSize(500, 450)

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
        self.change_password_button = QPushButton("Change Password")
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
        layout.addWidget(self.change_password_button)
        layout.addWidget(self.delete_data)
        layout.addWidget(self.reset_settings)
        layout.addWidget(self.close_settings)

        self.setLayout(layout)

        # Connections

        self.delete_data.clicked.connect(self.delete_data_function)
        self.change_password_button.clicked.connect(self.open_password_window)
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
        self.pass_window = ChangePasswordWindow(self.current_user)
        settings = fileHandling.load_settings(self.current_user)
        if settings:
            self.delete_data_on_exit.setChecked(settings.get("delete_on_exit", False))
            theme = settings.get("theme", "Default")
            self.themes.setCurrentText(theme)
            self.apply_theme(theme)

            self.big_text.setChecked(settings.get("big_text", False))
            self.bold_text.setChecked(settings.get("bold_text", False))

    def open_password_window(self):
        self.pass_window.show()

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
            "theme": self.themes.currentText(),
            "big_text": self.big_text.isChecked(),
            "bold_text": self.bold_text.isChecked()
        }
        fileHandling.save_settings(self.current_user, settings)
        theme = self.themes.currentText()
        self.theme_changed.emit(theme)
        self.text_changed.emit(self.big_text.isChecked(), self.bold_text.isChecked())
        self.close()

    def apply_text(self, big, bold):
        font = QFont()
        font.setPointSize(16 if big else 10)
        font.setBold(bold)
        self.setFont(font)

    def apply_theme(self, theme):

        big = fileHandling.load_settings(self.current_user).get("big_text", False)
        bold = fileHandling.load_settings(self.current_user).get("bold_text", False)

        font_size = 16 if big else 10
        font_boldness = "bold" if bold else "normal"

        if theme == "Dark":
            self.setStyleSheet(f"""
                        QWidget {{
                            background-color: #2a2a2a;
                            color: white;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QPushButton {{
                            background-color: #444;
                            color: white;
                            border: none;
                            padding: 5px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QComboBox {{
                            background-color: #444;
                            color: white;
                            border: none;
                            padding: 5px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                    """)
        elif theme == "Dark Blue":
            self.setStyleSheet(f"""
                        QWidget {{
                            background-color: #0d1b2a;
                            color: white;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QPushButton {{
                            background-color: #1a2640;
                            color: white;
                            border: none;
                            padding: 5px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QComboBox {{
                            background-color: #1a2640;
                            color: white;
                            border: none;
                            padding: 5px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                    """)
        elif theme == "Dark Purple":
            self.setStyleSheet(f"""
                        QWidget {{
                            background-color: #2b2d42;
                            color: white;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QPushButton {{
                            background-color: #5a5f9e;
                            color: white; 
                            border: none;
                            padding: 5px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QComboBox {{
                            background-color: #5a5f9e;
                            color: white; 
                            border: none;
                            padding: 5px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                    """)
        elif theme == "Eye Sore":
            self.setStyleSheet(f"""
                        QWidget {{
                            background-color: #fafefa;
                            color: #0000ff;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QPushButton {{
                            background-color: #ffaa00;
                            color: #0000ff; 
                            border: none;
                            padding: 1px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                        QComboBox {{
                            background-color: #ad72fe;
                            color: #00ff00; 
                            border: none;
                            padding: 2px;
                            font-size: {font_size}pt;
                            font-weight: {font_boldness};
                        }}
                    """)
        else:
            self.setStyleSheet("")

            if self.current_user:
                settings = fileHandling.load_settings(self.current_user)
                self.apply_text(settings.get("big_text", False), settings.get("bold_text", False))