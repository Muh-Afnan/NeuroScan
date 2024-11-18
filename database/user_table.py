import sqlite3
import bcrypt
from .database import DB_NAME

class UserDatabase:
    def __init__(self):
        self.db_name = DB_NAME
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.logged_in_user = None  # Store logged-in user
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                label_security_question TEXT NOT NULL,
                security_answer TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_user(self, username, password, label_security_question, security_answer):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, label_security_question, security_answer)
                VALUES (?, ?, ?, ?)
            ''', (username, hashed_password, label_security_question, security_answer))
            self.conn.commit()
            return {
                "status": True,
                "msg": f"User created, Username: '{username}'."
            }
        except sqlite3.IntegrityError:
            return {
                "status": False,
                "msg": f"Error: The username '{username}' is already taken."
            }

    def get_user_by_username(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def login(self, username, password):
        user = self.get_user_by_username(username)
        if user:
            stored_password = user[2]  # The hashed password is at index 2
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                self.logged_in_user = {
                    'id': user[0],
                    'username': user[1],
                    'label_security_question': user[3],
                    'security_answer': user[4]
                }
                return {
                    "status": True,
                    "msg": "Succefully Login"
                }
            else:
                return {
                    "status": False,
                    "msg": "Incorrect password."
                }
        else:
            return {
                "status": False,
                "msg": "Username not Found"
            }

    def get_logged_in_user(self):
        return self.logged_in_user

    def logout(self):
        self.logged_in_user = None

    def get_security_question(self, username):
        user = self.get_user_by_username(username)
        if user:
            security_question = user[3]
            return {
                "status": True,
                "msg": security_question
            }
        return {
            "status": False,
            "msg": "Username not Found"
        }

    # temporary
    def change_password(self, username, new_password):
        user = self.get_user_by_username(username)
        if user:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute('''
                UPDATE users
                SET password = ?
                WHERE username = ?
            ''', (hashed_password, username))
            self.conn.commit()
            print("Password updated successfully.")
        else:
            print("Username not found.")


    def change_password_by_answer(self, username, answer, new_password):
        user = self.get_user_by_username(username)
        if answer.strip().lower() == user[4].lower():
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute('''
                UPDATE users
                SET password = ?
                WHERE username = ?
            ''', (hashed_password, username))
            self.conn.commit()
            return {
                "status": True,
                "msg": "Password updated successfully."
            }
        else:
            return {
                "status": False,
                "msg": "Answer is Wrong."
            }
        
    def forgot_password(self, username, answer):
        user = self.get_user_by_username(username)
        if answer.strip().lower() == user[4].lower():
            return user[2]
        else:
            return False

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


