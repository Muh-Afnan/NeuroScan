import tkinter as tk  # Tkinter library ko import karte hain GUI banane ke liye
import os
from gui.login_frame import LoginFrame  # LoginFrame import karte hain (Login screen ke liye)
from gui.register_frame import RegisterFrame  # RegisterFrame import karte hain (Register screen ke liye)
from gui.main_frame import MainScreen  # MainScreen import karte hain (Main screen ke liye)
from gui.recover_password_frame import RecoverPasswordFrame  # RecoverPasswordFrame import karte hain (Password recovery ke liye)
from gui.train_frame import trainmodelframe  # TrainModelFrame import karte hain (Model training ke liye)
from gui.model_training_frame import modeltrainingscreen
from gui.detect_tumor import DetectTumor
from database.user_table import UserDatabase

class App(tk.Tk):
    def __init__(self):
        """
        Yeh constructor method hai jo application window ko initialize karta hai.
        Ismein window ka title, size, aur kuch instance variables set kiye gaye hain.
        `self.current_frame` variable current visible frame ko store karta hai.
        Application start hoti hi login screen show karta hai.
        """
        super().__init__()

        self.title("NeuroScan App")

        # Get screen width and height dynamically
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        self.geometry(f"{screen_width}x{screen_height}")
        self.state('zoomed')
        

        # File Paths and Directories
        self.dataset_path = ""
        self.training_dir = ""
        self.validation_dir = ""
        self.testing_dir = ""
        self.model_path = ""

        self.path = os.path.normpath(os.path.join("C:/", "NeuroScan")).replace("\\","/")
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.saved_model_path = os.path.normpath(os.path.join(self.path, "tumor_detection_model.pt")).replace("\\", "/")
        self.yaml_path = os.path.normpath(os.path.join(self.path,"Brain_Tumor_Detection.yaml")).replace('\\', '/')
        self.metrices_path = os.path.join(self.path, "Metrices/")
        if not os.path.exists(self.metrices_path):
            os.mkdir(self.metrices_path)
        self.tumor_detection_model_path = os.path.normpath(os.path.join(self.metrices_path, "tumor_detection_model")).replace('\\', '/')

        # Variables for tumor detection
        self.detect_tumor_image = ""
        self.image_paths = []
        self.label_path = []
        self.loaded_images = []
        self.loaded_labels = []
        self.dataset = 0
        self.metrices = None

        self.current_frame = None  # Currently visible frame ko store karta hai
        self.show_login()  # Login screen show karta hai jab app start hoti hai

        self.userdb = UserDatabase()

    def show_login(self):
        """
        Yeh method login screen ko display karta hai.
        Pehle screen clear ki jati hai, phir `LoginFrame` ko pack kiya jata hai.
        Ismein `self.show_register`, `self.show_main_screen`, aur `self.show_recover_password`
        functions ko as parameters pass kiya gaya hai taake un screens pe switch kiya ja sake.
        """
        self.clear_screen() 
        self.pack_screen(LoginFrame(self, self.show_register, self.show_main_screen, self.show_recover_password))

    def show_register(self):
        """
        Yeh method registration screen ko display karta hai.
        Pehle screen clear ki jati hai, phir `RegisterFrame` ko pack kiya jata hai.
        `self.show_login` ko as a parameter pass kiya gaya hai taake login screen pe wapas ja sake.
        """
        self.clear_screen()
        self.pack_screen(RegisterFrame(self, self.show_login))
    
    def show_main_screen(self):
        """
        Yeh method main application screen ko display karta hai.
        Pehle screen clear ki jati hai, phir `MainScreen` ko pack kiya jata hai.
        `self.show_train_frame` ko as a parameter pass kiya gaya hai taake training frame pe switch kiya ja sake.
        """
        self.clear_screen()
        self.pack_screen(MainScreen(self,self.show_train_frame,self.show_detect_tumor))

    def show_recover_password(self):
        """
        Yeh method password recovery screen ko display karta hai.
        Pehle screen clear ki jati hai, phir `RecoverPasswordFrame` ko pack kiya jata hai.
        `self.show_login` ko as a parameter pass kiya gaya hai taake login screen pe wapas ja sake.
        """
        self.clear_screen()
        self.pack_screen(RecoverPasswordFrame(self, self.show_login))

    def show_train_frame(self):
        """
        Yeh method model training screen ko display karta hai.
        Pehle screen clear ki jati hai, phir `trainmodelframe` ko pack kiya jata hai.
        `self.show_main_screen` ko as a parameter pass kiya gaya hai taake main screen pe wapas ja sake..
        """
        self.clear_screen()
        self.pack_screen(trainmodelframe(self, self.show_main_screen, self.show_model_training_frame))

    def show_model_training_frame(self):
        self.clear_screen()
        self.pack_screen(modeltrainingscreen(self, self.show_train_frame))

    def show_detect_tumor(self):
        self.clear_screen()
        self.pack_screen(DetectTumor(self, self.show_main_screen))

    def show_test_tumor(self):
        self.clear_screen()
        self.pack()

    def pack_screen(self, frame):
        """
        Yeh method kisi bhi frame ko screen pe display karne ke liye use hota hai.
        `frame` parameter new frame hota hai jo display hoga.
        Is function ke zariye current frame ko update kiya jata hai aur usko pack kiya jata hai.
        """
        self.current_frame = frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
    def clear_screen(self):
        """
        Yeh method current frame ko screen se hata deta hai.
        Agar koi frame already screen pe visible ho, to usko `pack_forget()` method ke zariye hide kiya jata hai.
        """
        if self.current_frame is not None:
            self.current_frame.pack_forget()

if __name__ == "__main__":
    app = App()  # App class ka instance create karte hain aur application run karte hain
    app.mainloop()