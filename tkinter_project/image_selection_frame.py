import tkinter as tk
from tkinter import ttk

class ImageSelectionFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Adding a style to the frame
        self.configure(style="ImageSelection.TFrame")

        ttk.Label(self, text="Select Medical Images", style="Title.TLabel").grid(row=0, column=0, columnspan=2)

        ttk.Button(self, text="Select Images", command=self.select_images, style="Button.TButton").grid(row=1, column=0, columnspan=2)

        ttk.Button(self, text="Detect Tumors", command=self.detect_tumors, style="Button.TButton").grid(row=2, column=0, columnspan=2)

        ttk.Button(self, text="Back to Login", command=self.controller.show_login_frame, style="Button.TButton").grid(row=3, column=0, columnspan=2)

    def select_images(self):
        try:
            # Image selection logic here
            tk.messagebox.showinfo("Image Selection", "Images selected successfully")
        except Exception as e:
            tk.messagebox.showerror("Image Selection Error", str(e))

    def detect_tumors(self):
        try:
            # Tumor detection logic here
            tk.messagebox.showinfo("Detection Result", "Tumor Detected / No Tumor Detected")
        except Exception as e:
            tk.messagebox.showerror("Detection Error", str(e))
