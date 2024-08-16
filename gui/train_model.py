import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import backend.backend as backend  # Importing the backend module

class train_model(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()


    def create_widgets(self):
        # Upload dataset button
        self.upload_button = tk.Button(self, text="Upload Dataset", command=self.upload_dataset)
        self.upload_button.pack(pady=10)

        # Preprocess data button
        self.preprocess_button = ttk.Button(self, text="Preprocess Data", command=self.preprocess_data)
        self.preprocess_button.pack(pady=10)

        # Augment data button
        self.augment_button = ttk.Button(self, text="Augment Data", command=self.augment_data)
        self.augment_button.pack(pady=10)

        # Select model button
        self.model_button = ttk.Button(self, text="Select Model", command=self.select_model)
        self.model_button.pack(pady=10)


    def upload_dataset(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            backend.handle_dataset_upload(filepath)

    def preprocess_data(self):
        backend.preprocess_data()

    def augment_data(self):
        backend.augment_data()

    def select_model(self):
        backend.select_model()