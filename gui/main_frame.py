import tkinter as tk
from tkinter import messagebox
import gui.train_frame as train_model
import database.query as Query

class MainScreen(tk.Frame):
    def __init__(self, master, show_train_frame, show_detect_tumor):
        """
        Constructor method jo MainScreen class ka instance banate waqt call hota hai.
        Parameters:
            - master: Tkinter window ya frame jisme yeh MainScreen attach hoga.
            - show_train_frame: Function jo training screen dikhane ke liye call hoga.
        """
        super().__init__(master)  # Parent class (tk.Frame) ka __init__ method call karte hain taake frame initialize ho jaye
        self.master = master  # Main application window ko store karte hain
        self.show_train_frame = show_train_frame  # Callback function jo training screen dikhane ke liye use hota hai
        self.show_detect_tumor = show_detect_tumor
        self.pack(fill=tk.BOTH, expand=True)  # MainScreen ko pack karte hain taake yeh available space ko fill kar sake

        self.configure_gui()  # GUI components ko configure karne ke liye method call karte hain

    def configure_gui(self):
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20, fill="x", expand=True)

        self.inner_frame = tk.Frame(button_frame)
        self.inner_frame.pack(expand=True)

        self.lable_title = tk.Label(self.inner_frame, text="Main Screen", font=("Arial",24), pady=20)
        self.lable_title.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        button_style_large = {"font": ("Arial",14), "width":15, "height":2, "padx":10, "pady":10}
        data = self.master.userdb.get_logged_in_user()    # def configure_gui(self):
        if data['user_type'] == 'admin':
            self.button_train_model = tk.Button(self.inner_frame, text="Train Model", **button_style_large, command=self.show_train_frame)
            self.button_train_model.grid(row=1, column=0, padx=10, pady=10)

        self.button_detect_tumor = tk.Button(self.inner_frame, text="Detect Tumor", **button_style_large, command=self.show_detect_tumor)
        self.button_detect_tumor.grid(row=1, column=1, padx=10, pady=10)

        self.button_logout = tk.Button(self.inner_frame, text="Logout", **button_style_large, command=self.logout)
        self.button_logout.grid(row=1, column=2, padx=10, pady=10)

    def logout(self):
        """
        Logout button click hone par call hota hai.
        Yeh method current screen ko hide karti hai aur login screen dikhane ke liye master window ka method call karti hai.
        """
        self.master.userdb.logout()
        self.pack_forget()  # Current screen ko hide karti hai
        self.master.show_login()  # Login screen dikhane ke liye master window ka method call karti hai
