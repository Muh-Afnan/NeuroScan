import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class RecoverPasswordFrame(tk.Frame):
    def __init__(self, master, show_login_callback):
        """
        Constructor method jo RecoverPasswordFrame class ka instance banate waqt call hota hai.
        Parameters:
            - master: Tkinter window ya frame jisme yeh RecoverPasswordFrame attach hoga.
            - show_login_callback: Function jo login screen dikhane ke liye call hota hai.
        """
        super().__init__(master)  # Parent class (tk.Frame) ka __init__ method call karte hain taake frame initialize ho jaye
        self.master = master  # Main application window ko store karte hain
        self.show_login_callback = show_login_callback  # Callback function jo login screen dikhane ke liye use hota hai
        self.create_widgets()  # GUI widgets create karne ke liye method call karte hain

    def create_widgets(self):
        """
        Yeh method GUI widgets ko create aur arrange karne ke liye use hoti hai.
        Isme labels, entry fields, dropdown menu, aur buttons create aur arrange kiye jaate hain.
        """
        # Username ke liye label create karte hain aur window mein add karte hain
        self.label_username = tk.Label(self, text="Username")
        self.label_username.pack(pady=10)

        # Username input field create karte hain jahan user apna username enter karega
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack(pady=10)

        # Button styles define karte hain
        button_style_small = {"font": ("Arial", 10), "width": 15, "height": 1, "padx": 5, "pady": 5}

        # Recover Password button create karte hain, command parameter se recover_password method call hoti hai
        self.button_recover = tk.Button(self, text="Get User", **button_style_small,
                                        command=self.recover_password)
        self.button_recover.pack(pady=10)

        # Back to Login button create karte hain, command parameter se show_login_callback method call hoti hai
        self.button_back_to_login = tk.Button(self, text="Back to Login", **button_style_small,
                                              command=self.show_login_callback)
        self.button_back_to_login.pack(pady=10)

    def show_answer(self, question):

        self.button_recover.destroy()
        self.button_back_to_login.destroy()

        self.label_security_answer = tk.Label(self, text=question)
        self.label_security_answer.pack(pady=5)

        self.entry_security_answer = ttk.Entry(self)
        self.entry_security_answer.pack(pady=10)


        self.new_password_label = tk.Label(self, text="New Password")
        self.new_password_label.pack(pady=10)

        self.entry_new_password = ttk.Entry(self, show="*")
        self.entry_new_password.pack(pady=10)

        button_style_small = {"font": ("Arial", 10), "width": 15, "height": 1, "padx": 5, "pady": 5}
        self.button_recover = tk.Button(self, text="Change Password", **button_style_small,
                                        command=self.change_password)
        self.button_recover.pack(pady=10)

        # Back to Login button create karte hain, command parameter se show_login_callback method call hoti hai
        self.button_back_to_login = tk.Button(self, text="Back to Login", **button_style_small,
                                              command=self.show_login_callback)
        self.button_back_to_login.pack(pady=10)


    def recover_password(self):
        """
        Recover Password button click hone par call hoti hai.
        Yeh method user se input le kar password recovery ke liye placeholder logic implement karti hai.
        """
        username = self.entry_username.get()  # Username ko get karte hain

        return_obj = self.master.userdb.get_security_question(username)
        if return_obj['status']:
            self.show_answer(return_obj['msg'])
        else: messagebox.showerror("Error", return_obj['msg'])


    def change_password(self):
        username = self.entry_username.get()
        security_answer = self.entry_security_answer.get()
        new_password = self.entry_new_password.get()

        return_obj = self.master.userdb.change_password_by_answer(username, security_answer, new_password)
        if return_obj['status']:
            messagebox.showinfo("Success", return_obj['msg'])
            self.show_login_callback()
        else: messagebox.showerror("Error", return_obj['msg'])
