from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit
from framework import userLogin

class ChangePasswordWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setWindowTitle("Change Password")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.label = QLabel(f"Change Password For {username}")

        self.old_input = QLineEdit()
        self.old_input.setPlaceholderText("Old Password")
        self.old_input.setEchoMode(QLineEdit.Password)

        self.new_input = QLineEdit()
        self.new_input.setPlaceholderText("New Password")
        self.new_input.setEchoMode(QLineEdit.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)

        self.confirm_button = QPushButton("Confirm Changes")

        layout.addWidget(self.label)
        layout.addWidget(self.old_input)
        layout.addWidget(self.new_input)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

        self.confirm_button.clicked.connect(self.pass_change)

    def pass_change(self):

        old_password = self.old_input.text()
        new_password = self.new_input.text()
        confirm_password = self.confirm_input.text()
        users = userLogin.load_users()

        if not old_password:
            QMessageBox.warning(self, "Error", "Please enter your password.")
            return

        if not new_password:
            QMessageBox.warning(self, "Error", "Please enter your new password.")
            return

        if len(new_password) < 6:
            QMessageBox.warning(self, "Error", "Password must be 6 characters or longer.")
            return

        if not confirm_password:
            QMessageBox.warning(self, "Error", "Please confirm your password.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Please ensure new passwords match.")
            return

        if not userLogin.check_password(old_password, users[self.username].encode()):
            QMessageBox.warning(self, "Error", "Old password is incorrect.")
            return

        new_hash = userLogin.hash_password(new_password).decode()
        users[self.username] = new_hash

        userLogin.save_users(users)

        QMessageBox.information(self, "Success", "Password has been changed.")
        self.close()

