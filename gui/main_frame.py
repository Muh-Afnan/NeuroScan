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
        """
        Yeh method GUI components ko configure karne ke liye use hoti hai.
        Isme labels aur buttons create aur arrange kiye jaate hain.
        """
        # Main title label create karte hain
        self.label_title = tk.Label(self, text="Main Screen", font=("Arial", 24), pady=20)
        self.label_title.pack()

        # Buttons ke liye ek frame create karte hain
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Button styles define karte hain
        button_style_large = {"font": ("Arial", 14), "width": 15, "height": 2, "padx": 10, "pady": 10}

        # Buttons create karte hain aur unko button_frame mein arrange karte hain

        data = self.master.userdb.get_logged_in_user()
        if data['user_type'] == 'admin':
            self.button_train_model = tk.Button(button_frame, text="Train Model", **button_style_large, command=self.show_train_frame)
            self.button_train_model.grid(row=0, column=0, padx=10, pady=10)

            self.button_test_model = tk.Button(button_frame, text="Test Model", **button_style_large, command=self.test_model)
            self.button_test_model.grid(row=0, column=1, padx=10, pady=10)

        # self.button_generate_matrix = tk.Button(button_frame, text="Confusion Matrix", **button_style_large, command=self.generate_matrix)
        # self.button_generate_matrix.grid(row=1, column=0, padx=10, pady=10)

        self.button_detect_tumor = tk.Button(button_frame, text="Detect Tumor", **button_style_large, command=self.show_detect_tumor)
        self.button_detect_tumor.grid(row=1, column=0, padx=10, pady=10)

        self.button_logout = tk.Button(button_frame, text="Logout", **button_style_large, command=self.logout)
        self.button_logout.grid(row=1, column=1, padx=10, pady=10)


    def test_model(self):
        """
        Test model button click hone par call hota hai.
        Yeh method ek info message show karti hai jo model testing ke process ko indicate karta hai.
        """
        messagebox.showinfo("Test Model", "Testing model...")

    def logout(self):
        """
        Logout button click hone par call hota hai.
        Yeh method current screen ko hide karti hai aur login screen dikhane ke liye master window ka method call karti hai.
        """
        self.master.userdb.logout()
        self.pack_forget()  # Current screen ko hide karti hai
        self.master.show_login()  # Login screen dikhane ke liye master window ka method call karti hai
