import sqlite3
from tkinter import *

# Function to create the database and table
def create_database():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            security_question TEXT,
            answer TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a user into the database
def insert_user(username, password, security_question, answer, role):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, security_question, answer, role)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, security_question, answer, role))
    conn.commit()
    conn.close()

# Function to save user data from the Tkinter form
def save_user():
    username = username_entry.get()
    password = password_entry.get()
    security_question = security_question_entry.get()
    answer = answer_entry.get()
    role = role_entry.get()
    insert_user(username, password, security_question, answer, role)

# Initialize the Tkinter window
root = Tk()
root.title("User Registration")

# Entry for username
Label(root, text="Username").pack()
username_entry = Entry(root)
username_entry.pack()

# Entry for password
Label(root, text="Password").pack()
password_entry = Entry(root, show='*')
password_entry.pack()

# Entry for security question
Label(root, text="Security Question").pack()
security_question_entry = Entry(root)
security_question_entry.pack()

# Entry for answer
Label(root, text="Answer").pack()
answer_entry = Entry(root)
answer_entry.pack()

# Entry for role
Label(root, text="Role").pack()
role_entry = Entry(root)
role_entry.pack()

# Save button to insert data into the database
save_button = Button(root, text="Save", command=save_user)
save_button.pack()

# Create the database and table before running the Tkinter mainloop
create_database()

# Run the Tkinter event loop
root.mainloop()
