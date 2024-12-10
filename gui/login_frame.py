import tkinter as tk  # Tkinter library ko import karte hain jo GUI banane ke liye use hoti hai
from tkinter import ttk, messagebox  # ttk module ko import karte hain jo additional GUI widgets provide karta hai

class LoginFrame(tk.Frame):
    def __init__(self, master, show_register_callback, show_main_screen_callback, show_recover_password_callback):
        """
        Constructor method jo LoginFrame class ka instance banane ke liye use hota hai.
        Parameters:
            - master: Tkinter window ya frame jisme yeh LoginFrame attach hoga.
            - show_register_callback: Function jo registration screen show karega.
            - show_main_screen_callback: Function jo main screen show karega jab login successful ho.
            - show_recover_password_callback: Function jo password recovery screen show karega.
        """
        super().__init__(master)  # Parent class (tk.Frame) ka __init__ method call karte hain

        self.master = master  # Main application window ko store karte hain
        # Callbacks ko store karte hain jo different screens show karne ke liye use honge
        self.show_register_callback = show_register_callback
        self.show_main_screen_callback = show_main_screen_callback
        self.show_recover_password_callback = show_recover_password_callback
        self.create_widgets()  # Widgets create karne ke liye method call karte hain

    def create_widgets(self):
        """
        Yeh method GUI widgets create karta hai jo login screen par display honge.
        Widgets mein labels, entry fields, aur buttons shamil hain.
        """
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

        # Button styles define karte hain taake buttons consistent aur aesthetic lagain
        button_style_small = {"font": ("Arial", 10), "width": 15, "height": 1, "padx": 5, "pady": 5}

        # Login button create karte hain, command parameter se button click hone par login method call hoti hai
        self.button_login = tk.Button(self, text="Login", **button_style_small, command=self.login)
        self.button_login.pack(pady=10)

        # Register Now button create karte hain, command parameter se button click hone par show_register_callback method call hoti hai
        self.button_register = tk.Button(self, text="Register Now", **button_style_small,
                                         command=self.show_register_callback)
        self.button_register.pack(pady=10)

        # Wide button style define karte hain jo recovery button ke liye use hoga
        button_style_wide = {"font": ("Arial", 10), "width": 20, "height": 1, "padx": 5, "pady": 5}

        # Recover Password button create karte hain, command parameter se button click hone par show_recover_password_callback method call hoti hai
        self.button_recover_password = tk.Button(self, text="Recover Password", **button_style_wide,
                                                 command=self.show_recover_password_callback)
        self.button_recover_password.pack(pady=10)

    def login(self):
        """
        Login method jo login button click hone par call hoti hai.
        Yeh method user ke entered username aur password ko check karta hai.
        Agar credentials sahi hote hain to main screen show karta hai, warna error message display hota hai.
        """
        username = self.entry_username.get()  # Username field se user ka input lete hain
        password = self.entry_password.get()  # Password field se user ka input lete hain

        login_obj = self.master.userdb.login(username, password)
        if login_obj['status']:
            messagebox.showinfo("Success", login_obj['msg'])
            self.show_main_screen_callback()
        else: messagebox.showerror("Error", login_obj['msg'])
