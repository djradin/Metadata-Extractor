import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox)
import basicFileInfo
import fileHandling
import userLogin
from gui.loginWIndow import LoginWindow


# Used a little GPT to get this to start working, since I am a little rusty on PySide6,
# mostly just bug spotting and workarounds, as well as connecting widgets to functions.
# detailed in my AI usage summary.

class MainWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window
        self.current_user = None
        self.setWindowTitle("File Tool")
        self.label = QLabel("No user logged in.")


        layout = QVBoxLayout()

        self.label = QLabel(f"Current user: {self.current_user}")

        self.diagnose_button = QPushButton("Diagnose File")
        self.load_button = QPushButton("Load File")
        self.logout_button = QPushButton("Log Out")

        layout.addWidget(self.label)
        layout.addWidget(self.diagnose_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

        self.diagnose_button.clicked.connect(self.diagnose_file)
        self.load_button.clicked.connect(self.load_file)
        self.logout_button.clicked.connect(self.logout)

    def set_current_user(self, username):
        self.current_user = username
        self.label.setText(f"Current user: {username}")

    def logout(self):
        self.current_user = None
        self.label.setText("No user logged in.")
        self.hide()
        self.login_window.show()
        self.login_window.username_input.clear()
        self.login_window.password_input.clear()


    def diagnose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")

        if not file_path:
            return

        metadata = basicFileInfo.diagnose_file(file_path)
        fileHandling.save_file(self.current_user, metadata)

        QMessageBox.information(self, "Success", "File processed and saved.")

    def load_file(self):
        files = fileHandling.list_files(self.current_user)

        if not files:
            QMessageBox.information(self, "Error", "No saved files found.")
            return

        from PySide6.QtWidgets import QInputDialog

        selected_file, ok = QInputDialog.getItem(
            self,"Select File","Choose a file:", files,0,False
        )

        if ok and selected_file:
            data = fileHandling.load_file(self.current_user, selected_file)
            QMessageBox.information(self, selected_file, str(data))



def run_app():
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    main_window = MainWindow(login_window)
    main_window.hide()  # hide until login succeeds

    def login_success(username):
        main_window.set_current_user(username)
        main_window.show()

    login_window.login_success.connect(login_success)
    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()