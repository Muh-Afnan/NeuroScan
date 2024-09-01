import tkinter as tk
from tkinter import ttk

class AdminFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Adding a style to the frame
        self.configure(style="Admin.TFrame")

        ttk.Label(self, text="Admin Panel", style="Title.TLabel").grid(row=0, column=0, columnspan=2)

        ttk.Button(self, text="Train Model", command=self.train_model, style="Button.TButton").grid(row=1, column=0, columnspan=2)

        ttk.Button(self, text="Test Model", command=self.test_model, style="Button.TButton").grid(row=2, column=0, columnspan=2)

        ttk.Button(self, text="Generate Confusion Matrix", command=self.generate_confusion_matrix, style="Button.TButton").grid(row=3, column=0, columnspan=2)

        ttk.Button(self, text="Adjust Metrics", command=self.adjust_metrics, style="Button.TButton").grid(row=4, column=0, columnspan=2)

        ttk.Button(self, text="Select Images", command=self.select_images, style="Button.TButton").grid(row=5, column=0, columnspan=2)

        ttk.Button(self, text="Detect Tumors", command=self.detect_tumors, style="Button.TButton").grid(row=6, column=0, columnspan=2)

        ttk.Button(self, text="Back to Login", command=self.controller.show_login_frame, style="Button.TButton").grid(row=7, column=0, columnspan=2)

    def train_model(self):
        try:
            # Model training logic here
            tk.messagebox.showinfo("Train Model", "Model trained successfully")
        except Exception as e:
            tk.messagebox.showerror("Train Model Error", str(e))

    def test_model(self):
        try:
            # Model testing logic here
            tk.messagebox.showinfo("Test Model", "Model tested successfully")
        except Exception as e:
            tk.messagebox.showerror("Test Model Error", str(e))

    def generate_confusion_matrix(self):
        try:
            # Confusion matrix generation logic here
            tk.messagebox.showinfo("Confusion Matrix", "Confusion matrix generated successfully")
        except Exception as e:
            tk.messagebox.showerror("Confusion Matrix Error", str(e))

    def adjust_metrics(self):
        try:
            # Metrics adjustment logic here
            tk.messagebox.showinfo("Adjust Metrics", "Metrics adjusted successfully")
        except Exception as e:
            tk.messagebox.showerror("Adjust Metrics Error", str(e))

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
