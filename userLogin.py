from typing import TextIO

import bcrypt
import json
import os

user_file = "users.json"

def load_users():
    if not os.path.exists(user_file):
        return {}

    with open(user_file, "r") as f:
        return json.load(f)

def save_users(users):
    with open(user_file, "w") as f:
        json.dump(users, f)

def login_start():

    users = load_users()

    if not users:
        print("No users found.")
        print("Please create an account")
        return create_user()

    choices = ["login", "create user", "delete account"]
    choice = ""

    while choice not in choices:
        choice = input("Please select: login, create user, delete account: ").lower()
    if choice == "login":
        return login("login")
    elif choice == "create user":
        create_user()
        return login("login")
    else:
        login("delete")
        return login_start()

def login(account_use):
    users = load_users()
    login_status = "unsuccessful"

    while login_status == "unsuccessful":
        username = input("Username: ")
        password = input("Password: ")

        if username not in users:
            print("User does not exist.")
            continue

        stored_hash = users[username].encode()

        if check_password(password, stored_hash):

            if account_use == "login":
                print(f"Login successful, welcome {username}.")
                login_status = "successful"
                return username
            elif account_use == "delete":
                print("Login successful, deleting account.")
                login_status = "successful"
                delete_account(username)
                return None

        else:
            print("Login failed.")


def create_user():
    # Loads the users to check the new user is unique
    users = load_users()

    # Sets password for the while loop so it doesn't just try once
    username = ""
    password = ""
    password_confirm = ""

    while username in users or username == "":
        username = input("Please enter a username for the account: ")

    while password == "" or password != password_confirm:
        password = input("Please enter a password for the account: ")
        password_confirm = input("Confirm password: ")

    hashed_password = hash_password(password).decode()
    users[username] = hashed_password
    save_users(users)
    print(f"The {username} account has been created, you can now log in.")
    login("login")
    return username

def delete_account(username):
    users = load_users()

    del users[username]
    save_users(users)
    print("Account deleted.")


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, stored_hash):
    return bcrypt.checkpw(password.encode(), stored_hash)

