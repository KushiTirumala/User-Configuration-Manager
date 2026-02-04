# User Configuration Manager

import json
import os

class User:
    def __init__(self, username, email, preferences):
        self.username = username
        self.email = email
        self.preferences = preferences

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "preferences": self.preferences
        }


class UserConfigManager:
    FILE_NAME = "users.json"

    def __init__(self):
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w") as f:
                json.dump([], f)

    def load_users(self):
        with open(self.FILE_NAME, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.FILE_NAME, "w") as f:
            json.dump(users, f, indent=4)

    def validate_user(self, user):
        if not user.username.strip():
            raise ValueError("Username cannot be empty")
        if "@" not in user.email:
            raise ValueError("Invalid email address")

    def add_user(self, user):
        self.validate_user(user)
        users = self.load_users()
        for u in users:
            if u["username"] == user.username:
                raise ValueError("User already exists")
        users.append(user.to_dict())
        self.save_users(users)

    def list_users(self):
        return self.load_users()

    def delete_user(self, username):
        users = self.load_users()
        users = [u for u in users if u["username"] != username]
        self.save_users(users)


def main():
    manager = UserConfigManager()
    while True:
        print("\nUser Configuration Manager")
        print("1. Add User")
        print("2. View Users")
        print("3. Delete User")
        print("4. Exit")
        choice = input("Choose an option: ")
        try:
            if choice == "1":
                username = input("Username: ")
                email = input("Email: ")
                theme = input("Preferred Theme (dark/light): ")
                language = input("Language: ")
                user = User(username, email, {"theme": theme, "language": language})
                manager.add_user(user)
                print("User added successfully")
            elif choice == "2":
                users = manager.list_users()
                if not users:
                    print("No users found")
                for u in users:
                    print(u)
            elif choice == "3":
                username = input("Enter username to delete: ")
                manager.delete_user(username)
                print("User deleted")
            elif choice == "4":
                break
            else:
                print("Invalid option")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
