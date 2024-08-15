import tkinter as tk  # Tkinter library ko import karte hain GUI banane ke liye
from gui.login_frame import LoginFrame  # LoginFrame import karte hain (Login screen ke liye)
from gui.register_frame import RegisterFrame  # RegisterFrame import karte hain (Register screen ke liye)
from gui.main_frame import MainScreen  # MainScreen import karte hain (Main screen ke liye)
from gui.recover_password_frame import RecoverPasswordFrame  # RecoverPasswordFrame import karte hain (Password recovery ke liye)
from gui.train_model import train_model  # RecoverPasswordFrame import karte hain (Password recovery ke liye)

# App class jo Tkinter ki main window ko manage karegi
class App(tk.Tk):
    def __init__(self):
        super().__init__()  # Parent class (Tk) ka __init__ method call kar rahe hain to initialize the window
        self.title("NeuroScan App")  # Window ka title set kar rahe hain
        self.geometry("800x600")  # Window ki width 800 aur height 600 pixels set kar rahe hain

        self.current_frame = None  # Yeh variable track karega ke kaunsa screen (frame) currently dikh raha hai
        # self.show_register()
        self.show_login()  # App start hone par sabse pehle login screen dikhate hain

    # Yeh method login screen ko display karne ke liye hai
    def show_login(self):
        # Agar koi screen currently display ho rahi hai, usko hide kar dete hain
        if self.current_frame is not None:
            self.current_frame.pack_forget()  # pack_forget() method se current screen ko hide kar dete hain

        # Login screen banate hain aur usko current frame ke variable mein store karte hain
        # self.current_frame = LoginFrame(self, self.show_register, self.show_main_screen, self.show_recover_password)
        self.current_frame = LoginFrame(self, self.show_register, self.show_main_screen, self.show_recover_password)
        self.current_frame.pack()  # Login screen ko window mein dikhate hain

    # Yeh method register screen ko display karne ke liye hai
    def show_register(self):
        # Agar koi screen currently display ho rahi hai, usko hide kar dete hain
        if self.current_frame is not None:
            self.current_frame.pack_forget()  # pack_forget() method se current screen ko hide kar dete hain

        # Register screen banate hain aur usko current frame ke variable mein store karte hain
        self.current_frame = RegisterFrame(self, self.show_login)
        self.current_frame.pack(fill=tk.BOTH, expand=True)  # Register screen ko window mein dikhate hain
    
    # def train_model(self):
    #     if self.current_frame is not None:
    #         self.current_frame.pack_forget()
            
    #     self.current_frame =  train_model.train_model(self)
    #     self.current_frame.pack()

    # Yeh method main screen ko display karne ke liye hai
    def show_main_screen(self):
        # Agar koi screen currently display ho rahi hai, usko hide kar dete hain
        if self.current_frame is not None:
            self.current_frame.pack_forget()  # pack_forget() method se current screen ko hide kar dete hain

        # Main screen banate hain aur usko current frame ke variable mein store karte hain
        self.current_frame = MainScreen(self)
        self.current_frame.pack()  # Main screen ko window mein dikhate hain

    # Yeh method password recovery screen ko display karne ke liye hai
    def show_recover_password(self):
        # Agar koi screen currently display ho rahi hai, usko hide kar dete hain
        if self.current_frame is not None:
            self.current_frame.pack_forget()  # pack_forget() method se current screen ko hide kar dete hain

        # Password recovery screen banate hain aur usko current frame ke variable mein store karte hain
        self.current_frame = RecoverPasswordFrame(self, self.show_login)
        self.current_frame.pack()  # Password recovery screen ko window mein dikhate hain

# Yeh block ensure karta hai ke app sirf tab run ho jab is file ko direct execute kiya jaye
if __name__ == "__main__":
    app = App()  # App class ka ek instance banate hain
    app.mainloop()  # Tkinter ka main loop start karte hain, jo window ko display aur interact karne ke liye zaroori hai
