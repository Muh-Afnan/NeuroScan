import tkinter as tk  # Tkinter library ko import karte hain GUI banane ke liye
from gui.login_frame import LoginFrame  # LoginFrame import karte hain (Login screen ke liye)
from gui.register_frame import RegisterFrame  # RegisterFrame import karte hain (Register screen ke liye)
from gui.main_frame import MainScreen  # MainScreen import karte hain (Main screen ke liye)
from gui.recover_password_frame import RecoverPasswordFrame  # RecoverPasswordFrame import karte hain (Password recovery ke liye)
from gui.train_model import train_model  # RecoverPasswordFrame import karte hain (Password recovery ke liye)

class App(tk.Tk):
    def __init__(self):
        super().__init__() 
        self.title("NeuroScan App")  
        self.geometry("800x600")

        self.current_frame = None  
        self.show_login()  

    def show_login(self):
        self.clear_screen() 
        self.pack_screen(LoginFrame(self, self.show_register, self.show_main_screen, self.show_recover_password))

    def show_register(self):
        self.clear_screen()
        self.pack_screen(RegisterFrame(self, self.show_login))
    
    def show_main_screen(self):
        self.clear_screen()
        self.pack_screen(MainScreen(self,self.show_train_model))

    def show_recover_password(self):
        self.clear_screen()
        self.pack_screen(RecoverPasswordFrame(self, self.show_login))

    def show_train_model(self):
        self.clear_screen()
        self.pack_screen(train_model(self,self.show_main_screen))

    def pack_screen(self,frame):
        self.current_frame = frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
    def clear_screen(self):
        if self.current_frame is not None:
            self.current_frame.pack_forget()

if __name__ == "__main__":
    app = App()  
    app.mainloop()