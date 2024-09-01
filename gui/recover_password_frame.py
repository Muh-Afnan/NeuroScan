import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class RecoverPasswordFrame(tk.Frame):
    def __init__(self, master, show_login_callback):
        super().__init__(master)
        self.master = master
        self.show_login_callback = show_login_callback
        self.create_widgets()

    def create_widgets(self):
        self.label_username = tk.Label(self, text="Username")
        self.label_username.pack(pady=10)

        self.entry_username = ttk.Entry(self)
        self.entry_username.pack(pady=10)

        self.label_security_question = tk.Label(self, text="Select your security question")
        self.label_security_question.pack(pady=10)

        self.security_questions = [
            "What is your pet's name?",
            "What is your mother's maiden name?",
            "What was your first car?",
            "What elementary school did you attend?",
            "What is your favorite food?"
        ]

        self.default_val = tk.StringVar()
        self.default_val.set("Select a question")
        self.question_drop_down = tk.OptionMenu(self, self.default_val, *self.security_questions)
        self.question_drop_down.pack(pady=10)
        

        self.label_security_answer = tk.Label(self, text="Answer")
        self.label_security_answer.pack(pady=10)

        self.entry_security_answer = ttk.Entry(self)
        self.entry_security_answer.pack(pady=10)

        button_style_small = {"font": ("Arial", 10), "width": 15, "height": 1, "padx": 5, "pady": 5}

        self.button_recover = tk.Button(self, text="Recover Password", **button_style_small,
                                        command=self.recover_password)
        self.button_recover.pack(pady=10)

        self.button_back_to_login = tk.Button(self, text="Back to Login", **button_style_small,
                                              command=self.show_login_callback)
        self.button_back_to_login.pack(pady=10)

    def recover_password(self):
        username = self.entry_username.get()
        security_question = self.default_val.get()
        print(security_question)
        security_answer = self.entry_security_answer.get()

        # Placeholder logic for password recovery
        # if username and security_question != "Select a question" and security_answer:
        #     messagebox.showinfo("Recover Password", "Password recovery successful (simulated).")
        #     self.show_login_callback()
        # else:
        #     messagebox.showerror("Error", "Please complete all fields.")
