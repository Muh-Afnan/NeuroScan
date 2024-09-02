import tkinter as tk  # Tkinter library ko import karte hain jo GUI banane ke liye use hoti hai
from tkinter import ttk  # ttk module ko import karte hain jo additional GUI widgets provide karta hai
import database.query as Query

class LoginFrame(tk.Frame):  # LoginFrame class ko define karte hain jo tk.Frame se inherit karti hai
    def __init__(self,master,show_register_callback, show_main_screen_callback, show_recover_password_callback):
        # Constructor method jo class ka instance banane ke liye use hota hai
        super().__init__(master)  # Parent class (tk.Frame) ka __init__ method call karte hain

        self.master = master  # Main application window ko store karte hain
        # Callbacks ko store karte hain jo different screens show karne ke liye use honge
        self.show_register_callback = show_register_callback
        self.show_main_screen_callback = show_main_screen_callback
        self.show_recover_password_callback = show_recover_password_callback
        self.create_widgets()  # Widgets create karne ke liye method call karte hain

    def create_widgets(self):
        # Yeh method GUI widgets create karne ke liye hai

        # Username label create karte hain aur window mein add karte hain
        self.label_username = tk.Label(self, text="Username")
        self.label_username.pack(pady=10)  # pady se vertical spacing add karte hain

        # Username entry field create karte hain jahan user apna username enter karega
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack(pady=10)

        # Password label create karte hain aur window mein add karte hain
        self.label_password = tk.Label(self, text="Password")
        self.label_password.pack(pady=10)

        # Password entry field create karte hain jahan user apna password enter karega
        # show="*" se password ko hide karte hain
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack(pady=10)

        # Button styles define karte hain
        button_style_small = {"font": ("Arial", 10), "width": 15, "height": 1, "padx": 5, "pady": 5}

        # Login button create karte hain, command parameter se button click hone par login method call hoti hai
        self.button_login = tk.Button(self, text="Login", **button_style_small, command=self.login)
        self.button_login.pack(pady=10)

        # Register Now button create karte hain, command parameter se button click hone par show_register_callback method call hoti hai
        self.button_register = tk.Button(self, text="Register Now", **button_style_small,
                                         command=self.show_register_callback)
        self.button_register.pack(pady=10)

        # Wide button style define karte hain
        button_style_wide = {"font": ("Arial", 10), "width": 20, "height": 1, "padx": 5, "pady": 5}

        # Recover Password button create karte hain, command parameter se button click hone par show_recover_password_callback method call hoti hai
        self.button_recover_password = tk.Button(self, text="Recover Password", **button_style_wide,
                                                 command=self.show_recover_password_callback)
        self.button_recover_password.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Loggin Authentication

        # if Query.login_query(username, password):
        #     self.show_main_screen_callback()
        # else:
        #     tk.messagebox.showinfo("Error","Username or Password Error.Please Try Again")

        # print(username)
        # Login method jo login button click hone par call hoti hai
        # Yeh method main screen ko show karne ke liye show_main_screen_callback method call karti hai
        self.show_main_screen_callback()
