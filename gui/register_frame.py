import tkinter as tk  # Tkinter library ko import karte hain jo GUI (Graphical User Interface) banane ke liye use hoti hai
from tkinter import ttk, messagebox  # ttk module ko import karte hain jo additional widgets aur styling options provide karta hai
class RegisterFrame(tk.Frame):  # RegisterFrame class define karte hain jo tk.Frame se inherit karti hai
    def __init__(self, master, show_login_callback):
        """
        Constructor method jo RegisterFrame class ka instance banate waqt call hota hai.
        Parameters:
            - master: Tkinter window ya frame jisme yeh RegisterFrame attach hoga.
            - show_login_callback: Function jo login screen dikhane ke liye call hoga.
        """
        super().__init__(master)  # Parent class (tk.Frame) ka __init__ method call karte hain taake frame initialize ho jaye
        self.master = master  # Main application window ko store karte hain
        self.show_login_callback = show_login_callback  # Callback function ko store karte hain jo login screen dikhane ke liye use hota hai
        self.create_widgets()  # Widgets create karne ke liye method call karte hain

    def create_widgets(self):
        """
        Yeh method GUI widgets ko create karne aur arrange karne ke liye use hota hai.
        Isme labels, entry fields, combobox, aur buttons include hote hain.
        """
        # Username ke liye label create karte hain aur window mein add karte hain
        self.label_username = tk.Label(self, text="Username")
        self.label_username.pack(pady=10)  # pady=10 se vertical spacing add karte hain

        # Username input field create karte hain jahan user apna username enter karega
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack(pady=10)

        # Password ke liye label create karte hain aur window mein add karte hain
        self.label_password = tk.Label(self, text="Password")
        self.label_password.pack(pady=10)

        # Password input field create karte hain jahan user apna password enter karega
        # show="*" se password characters ko hide karte hain
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack(pady=10)

        # Security question ke liye label create karte hain
        self.label_security_question = tk.Label(self, text="Select a security question")
        self.label_security_question.pack(pady=10)

        # Security questions ka list banate hain jo user choose kar sakta hai
        self.security_questions = [
            "What is your pet's name?",
            "What is your mother's maiden name?",
            "What was your first car?",
            "What elementary school did you attend?",
            "What is your favorite food?"
        ]

        # Combobox create karte hain jahan security questions ka list dikhaya jayega
        self.default_val = tk.StringVar()
        self.question_drop_down = tk.OptionMenu(self, self.default_val, *self.security_questions)
        self.question_drop_down.pack(pady=10)
        self.default_val.set("Select a question")  # Default option set karte hain

        # Security answer ke liye label create karte hain
        self.label_security_answer = tk.Label(self, text="Answer")
        self.label_security_answer.pack(pady=10)

        # Security answer input field create karte hain jahan user apna answer enter karega
        self.entry_security_answer = tk.Entry(self)
        self.entry_security_answer.pack(pady=10)

        # Button styles define karte hain jo consistent button appearance ke liye use hoti hain
        button_style_small = {"font": ("Arial", 10), "width": 10, "height": 1, "padx": 5, "pady": 5}

        # Register button create karte hain jo click hone par register method call karega
        self.button_register = tk.Button(self, text="Register", **button_style_small, command=self.register)
        self.button_register.pack(pady=10)
        
        # Back to Login button create karte hain jo click hone par login screen dikhane ke liye show_login_callback ko call karega
        self.button_back_to_login = tk.Button(self, text="Back to Login", **button_style_small,
                                              command=self.show_login_callback)
        self.button_back_to_login.pack(pady=10)

    def register(self):
        """
        Register method jo Register button click hone par call hota hai.
        Yeh method user ke entered data ko retrieve karta hai aur future implementation ke liye ready karta hai.
        """
        username = self.entry_username.get()  # Username field se user ka input lete hain
        password = self.entry_password.get()  # Password field se user ka input lete hain
        selected_question = self.default_val.get()  # Selected security question ko retrieve karte hain
        answer = self.entry_security_answer.get()
        return_obj = self.master.userdb.insert_user(username, password, selected_question, answer)
        if return_obj['status']:
            messagebox.showinfo("Success", return_obj['msg'])
        else: messagebox.showerror("Error", return_obj['msg'])

        self.entry_username.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_security_answer.delete(0, 'end')
        self.default_val.set("Select a question")

