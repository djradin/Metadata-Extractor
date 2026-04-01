import sys, json, fileHandling, basicFileInfo
from textwrap import indent

from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QFileDialog, QMessageBox, QSplitter, QListWidget)
from gui.loginWIndow import LoginWindow
from gui.settingsWindow import SettingsWindow


# Used a little GPT to get this to start working, since I am a little rusty on PySide6,
# mostly just bug spotting and workarounds, as well as connecting widgets to functions.
# detailed in my AI usage summary.

class MainWindow(QWidget):
    def __init__(self, login_window, settings_window):
        super().__init__()

        self.login_window = login_window
        self.settings_window = settings_window
        self.current_user = None
        self.setWindowTitle("File Tool")

        # Top bar
        top_layout = QHBoxLayout()

        self.label = QLabel("No user logged in.")
        self.settings_button = QPushButton("Settings")
        self.logout_button = QPushButton("Log out")

        top_layout.addWidget(self.label)
        top_layout.addStretch()
        top_layout.addWidget(self.settings_button)
        top_layout.addWidget(self.logout_button)

        # Splitter Setup

        main_splitter = QSplitter(Qt.Horizontal)

        # Left side

        left_widget = QWidget()
        left_layout = QVBoxLayout()

        self.diagnose_button = QPushButton("Add File")
        self.file_list = QListWidget()

        left_layout.addWidget(self.label)
        left_layout.addWidget(self.diagnose_button)
        left_layout.addWidget(QLabel("Saved Files"))
        left_layout.addWidget(self.file_list)

        left_widget.setLayout(left_layout)

        # Right Side

        right_widget = QWidget()
        right_layout = QVBoxLayout()

        self.display = QTextEdit()
        self.display.setReadOnly(True)

        right_layout.addWidget(QLabel("File Info"))
        right_layout.addWidget(self.display)
        right_widget.setLayout(right_layout)

        # Splitter

        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([250, 500])

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(main_splitter)

        self.setLayout(main_layout)


        # Connections

        self.diagnose_button.clicked.connect(self.diagnose_file)
        self.logout_button.clicked.connect(self.logout)
        self.file_list.itemClicked.connect(self.show_file)
        self.settings_button.clicked.connect(self.settings)

    def set_current_user(self, username):
        self.current_user = username
        self.label.setText(f"Current user: {username}")
        self.pop_file_list()
        settings = fileHandling.load_settings(username)
        if settings:
            theme = settings.get("theme", "Default")
            self.apply_theme(theme)

    def logout(self):
        self.current_user = None
        self.label.setText("No user logged in.")
        self.hide()
        self.login_window.show()
        self.login_window.username_input.clear()
        self.login_window.password_input.clear()

    def settings(self):
        self.settings_window.set_current_user(self.current_user)
        self.settings_window.show()

    def diagnose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")

        if not file_path:
            return

        metadata = basicFileInfo.diagnose_file(file_path)
        fileHandling.save_file(self.current_user, metadata)

        QMessageBox.information(self, "Success", "File processed and saved.")

        self.pop_file_list()

    def pop_file_list(self):
        self.file_list.clear()

        files = fileHandling.list_files(self.current_user)

        for f in files:
            self.file_list.addItem(f)

    def show_file(self, item):
        filename = item.text()
        data = fileHandling.load_file(self.current_user, filename)

        if data:
            formatted = "\n".join(self.format_data(data))
            self.display.setText(formatted)

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

    def format_data(self, data, indent = 0):
        lines = []

        prefix = " " * indent

        if isinstance(data,dict):
            for k, v in data.items():
                readable_key = k.replace("_", " ").title()
                if isinstance(v, (dict, list)):
                    lines.append(f"{prefix}{readable_key}:")
                    lines.extend(self.format_data(v, indent + 4))
                else:
                    lines.append(f"{prefix}- {readable_key}: {v}")
        elif isinstance(data,list):
            for i, item in enumerate(data):
                lines.append(f"{prefix}- Item {i+1}:")
                lines.extend(self.format_data(item, indent + 4))
        else:
            lines.append(f"{prefix}- {data}")
        return lines


    def closeEvent(self, event):
        if self.settings_window.delete_data_on_exit.isChecked():
            print("close event triggered.")
            if self.current_user:
                fileHandling.delete_folder(self.current_user)

        event.accept()







def run_app():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    settings_window = SettingsWindow()
    main_window = MainWindow(login_window, settings_window)
    main_window.hide()  # hide until login succeeds
    settings_window.theme_changed.connect(main_window.apply_theme)

    def login_success(username):
        main_window.set_current_user(username)
        main_window.show()

    login_window.login_success.connect(login_success)
    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()