import tkinter as tk
from Implementation.preprocessing_data import resize_data,normalize_data

class PreprocessingFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.resize_data = resize_data
        self.normalize_data = normalize_data

        self.create_interface()

    def create_interface(self):
        self.second_window = tk.Toplevel(self)
        self.second_window.title("Data Preprocessing")
        self.second_window.geometry("800x500")
        
        self.progress_bar = tk
        self.inner_frame = tk.Frame(self.second_window)
        self.inner_frame.pack()

        button_style_large = {"font": ("Arial", 14), "width": 15, "height": 2, "padx": 10, "pady": 10}

        self.resize_button = tk.Button(self.inner_frame, text="Resize Data Set", **button_style_large, command = self.resize_data)
        self.resize_button.grid(row=0, column=0,padx=10, pady=10)

        self.normalize_data = tk.Button(self.inner_frame, text="Normalize Data Set", **button_style_large, command = self.normalize_data)
        self.normalize_data.grid(row=0, column=1,padx=10, pady=10)