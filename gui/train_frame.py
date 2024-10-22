import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk
from Implementation.backend import load_images_from_folder, augment_image
from gui.preprocessing_frame import PreprocessingFrame
from gui.augment_frame import AugmentFrame
import os

class trainmodelframe(tk.Frame):
    def __init__(self, mainapp, show_main_screen):
        """
        Constructor method jo trainmodelframe class ka instance banate waqt call hota hai.
        Parameters:
            - master: Tkinter window ya frame jisme yeh trainmodelframe attach hoga.
            - show_main_screen: Function jo main screen dikhane ke liye call hota hai.
        """
        super().__init__(mainapp)
        self.mainapp_obj = mainapp
        self.callback_main_Screen = show_main_screen

        # # Initialize dataset path, image paths, and loaded images
        # self.master.dataset_path = ""
        # self.master.image_paths = []
        # self.master.loaded_images = []
        # self.create_widgets()

    def create_widgets(self):
        """
        Yeh method GUI widgets ko create aur arrange karne ke liye use hoti hai.
        Isme buttons aur labels create aur arrange kiye jaate hain.
        """
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20, fill="x", expand=True)

        # Add another frame inside `button_frame` to center the buttons horizontally
        inner_frame = tk.Frame(button_frame)
        inner_frame.pack(expand=True)

        # Button styles define karte hain
        button_style_large = {"font": ("Arial", 14), "width": 15, "height": 2, "padx": 10, "pady": 10}

        # Back button to return to the main screen
        self.back_button = tk.Button(inner_frame, text="Back to Main", command=self.callback_main_Screen)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Label to show dataset information
        self.dataset_info_label = tk.Label(inner_frame, text="No dataset loaded")
        self.dataset_info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Button to upload dataset
        self.upload_button = tk.Button(inner_frame, text="Upload Dataset", **button_style_large, command=self.upload_dataset)
        self.upload_button.grid(row=2, column=0, padx=10, pady=10)

        # Button to preprocess data
        self.preprocess_button = tk.Button(inner_frame, text="Preprocess Data", **button_style_large, command=self.call_preprocessingframe)
        self.preprocess_button.grid(row=2, column=1, padx=10, pady=10)

        # Button to augment data
        self.augment_button = tk.Button(inner_frame, text="Augment Data", **button_style_large, command=self.call_augmentation_frame)
        self.augment_button.grid(row=3, column=0, padx=10, pady=10)

        # Button to select model
        self.select_model_button = tk.Button(inner_frame, text="Select Model", **button_style_large, command=self.select_model)
        self.select_model_button.grid(row=3, column=1, padx=10, pady=10)



    def upload_dataset(self):
        """
        This method is called when the Upload button is clicked.
        It opens a dialog to select a dataset folder and loads the images.
        """
        # Open a dialog to select a folder and store the path
        dataset_folder = filedialog.askdirectory(title="Select Dataset Folder")
        
        if dataset_folder:
            # Get all image file paths in the folder
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            image_paths = [os.path.join(dataset_folder, f) for f in os.listdir(dataset_folder) if f.lower().endswith(image_extensions)]
        

            # Update the UI with dataset information
            self.dataset_info_label.config(text=f"Dataset loaded from: {dataset_folder}\nNumber of images: {num_images}")
            
            # Show a message box with the dataset details
            messagebox.showinfo("Dataset Uploaded", f"Dataset uploaded from: {dataset_folder}\nNumber of images: {num_images}")
            
            # Store paths and images for later use
            self.mainapp_obj.dataset_path = dataset_folder
            self.mainapp_obj.image_paths = image_paths
        else:
            messagebox.showwarning("No Dataset", "Please select a valid dataset folder.")

    def call_preprocessingframe(self,mainapp_obj):
        """
        Preprocess button click hone par call hoti hai.
        Yeh method ek new window open karti hai jahan data preprocessing ke options hote hain.
        """
        if not self.mainapp_obj.dataset_path:
            messagebox.showwarning("No Dataset", "Please upload a dataset first.")
            return
        PreprocessingFrame(self,mainapp_obj)

    def call_augmentation_frame(self):
        """
        Augment button click hone par call hoti hai.
        Yeh method ek new window open karti hai jahan data augmentation ke options hote hain.
        """
        if not self.master.dataset_path:
            messagebox.showwarning("No Dataset", "Please upload a dataset first.")
            return

        augment_window = tk.Toplevel(self)
        augment_window.title("Data Augmentation")
        augment_window.geometry("1200x800")
        AugmentFrame(self,augment_window)
