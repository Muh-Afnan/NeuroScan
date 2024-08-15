import tkinter as tk
from tkinter import ttk

def configure_styles():
    # Configure main styles
    ttk.Style().configure("Main.TFrame", background="white")
    ttk.Style().configure("Title.TLabel", font=("Arial", 20, "bold"), foreground="blue")
    ttk.Style().configure("Label.TLabel", font=("Arial", 12), foreground="black")
    ttk.Style().configure("Button.TButton", font=("Arial", 12, "bold"), foreground="white", background="blue")

    # Configure frame-specific styles
    ttk.Style().configure("Login.TFrame", padding=(20, 20, 20, 20))
    ttk.Style().configure("Register.TFrame", padding=(20, 20, 20, 20))
    ttk.Style().configure("ImageSelection.TFrame", padding=(20, 20, 20, 20))
    ttk.Style().configure("Admin.TFrame", padding=(20, 20, 20, 20))
