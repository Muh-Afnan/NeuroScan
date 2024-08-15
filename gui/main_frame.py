import tkinter as tk
from tkinter import messagebox
# import train_model as tm
import database.query as Query

class MainScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        self.configure_gui()

    def configure_gui(self):
        self.label_title = tk.Label(self, text="Admin Main Screen", font=("Arial", 24), pady=20)
        self.label_title.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        button_style_large = {"font": ("Arial", 14), "width": 15, "height": 2, "padx": 10, "pady": 10}

        self.button_train_model = tk.Button(button_frame, text="Train Model", **button_style_large, command=self.train_model)
        self.button_train_model.grid(row=0, column=0, padx=10, pady=10)

        self.button_test_model = tk.Button(button_frame, text="Test Model", **button_style_large, command=self.test_model)
        self.button_test_model.grid(row=0, column=1, padx=10, pady=10)

        self.button_generate_matrix = tk.Button(button_frame, text="Confusion Matrix", **button_style_large, command=self.generate_matrix)
        self.button_generate_matrix.grid(row=0, column=2, padx=10, pady=10)

        self.button_adjust_metrics = tk.Button(button_frame, text="Adjust Metrics", **button_style_large, command=self.adjust_metrics)
        self.button_adjust_metrics.grid(row=1, column=0, padx=10, pady=10)

        self.button_detect_tumor = tk.Button(button_frame, text="Detect Tumor", **button_style_large, command=self.detect_tumor)
        self.button_detect_tumor.grid(row=1, column=1, padx=10, pady=10)

        self.button_logout = tk.Button(button_frame, text="Logout", **button_style_large, command=self.logout)
        self.button_logout.grid(row=1, column=2, padx=10, pady=10)

    def train_model(self):
        messagebox.showinfo("Train Model", "Training model...")

    def test_model(self):
        messagebox.showinfo("Test Model", "Testing model...")

    def generate_matrix(self):
        messagebox.showinfo("Generate Confusion Matrix", "Generating confusion matrix...")

    def adjust_metrics(self):
        messagebox.showinfo("Adjust Metrics", "Adjusting metrics...")

    def detect_tumor(self):
        messagebox.showinfo("Detect Tumor", "Detecting tumor...")

    def logout(self):
        self.pack_forget()
        self.master.show_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainScreen(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
