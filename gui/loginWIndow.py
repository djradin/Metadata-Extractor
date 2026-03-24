import sys
from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PySide6.QtCore import Signal
import userLogin, fileHandling

class LoginWindow(QWidget):

    login_success = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign In")

        layout = QVBoxLayout()

        self.label_info = QLabel("Please log in to your account to continue.")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.create_account_button = QPushButton("Create Account")
        self.delete_account_button = QPushButton("Delete Account")

        layout.addWidget(self.label_info)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.create_account_button)
        layout.addWidget(self.delete_account_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        self.create_account_button.clicked.connect(self.create_account)
        self.delete_account_button.clicked.connect(self.delete_account)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        users = userLogin.load_users()
        try:
            stored_hash = users[username].encode()
        except UnboundLocalError:
            QMessageBox.warning(self, "Error", "Please enter a username.")
            return
        except KeyError:
            QMessageBox.warning(self, "Error","Login failed.")
            return

        if userLogin.check_password(password, stored_hash):
            QMessageBox.information(self, "Login Successful", f"Login Successful, welcome {username}.")
            self.login_success.emit(username)
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed.", "Login Unsuccessful.")

        if username not in users:
            QMessageBox.warning(self, "Login Failed", "User does not exist.")

    def create_account(self):
        username = self.username_input.text()
        password = self.username_input.text()

        users = userLogin.load_users()

        if username in users:
            QMessageBox.warning(self, "Error", "User already taken.")
            return

        if not username:
            QMessageBox.warning(self, "Error", "Username cannot be left blank.")
            return

        if not password:
            QMessageBox.warning(self, "Error", "Password cannot be left blank.")
            return

        if username  == "Sheldon":
            QMessageBox.warning(self, "Bazinga", "Bazinga")
            return

        hashed_password = userLogin.hash_password(password).decode()
        users[username] = hashed_password
        userLogin.save_users(users)
        QMessageBox.information(self, "Account Created.", "Your account has been created, you can now log in.")

    def delete_account(self):

        username = self.username_input.text()
        password = self.username_input.text()



        users = userLogin.load_users()

        if username not in users:
            QMessageBox.warning(self, "Error", "User does not exist.")
            return

        stored_hash = users[username].encode()


        if userLogin.check_password(password, stored_hash):
            fileHandling.delete_folder(username)
            del users[username]
            userLogin.save_users(users)

            QMessageBox.information(self, "Success", f"Account '{username}' deleted")
        else:
            QMessageBox.warning(self, "Error", "Incorrect password.")