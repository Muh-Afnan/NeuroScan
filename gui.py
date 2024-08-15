import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import backend  # Importing the backend module

def upload_dataset():
    filepath = filedialog.askopenfilename()
    if filepath:
        backend.handle_dataset_upload(filepath)

def preprocess_data():
    backend.preprocess_data()

def augment_data():
    backend.augment_data()

def select_model():
    backend.select_model()

# Main window
root = tk.Tk()
root.title("Deep Learning Preprocessing and Model Selection")
root.geometry("400x300")

# Upload dataset button
upload_button = ttk.Button(root, text="Upload Dataset", command=upload_dataset)
upload_button.pack(pady=10)

# Preprocess data button
preprocess_button = ttk.Button(root, text="Preprocess Data", command=preprocess_data)
preprocess_button.pack(pady=10)

# Augment data button
augment_button = ttk.Button(root, text="Augment Data", command=augment_data)
augment_button.pack(pady=10)

# Select model button
model_button = ttk.Button(root, text="Select Model", command=select_model)
model_button.pack(pady=10)

root.mainloop()
