import tkinter as tk
from PIL import ImageTk
from Implementation.train_code import LoadDataset

class trainmodelframe(tk.Frame):
    def __init__(self, mainapp, show_main_screen, show_model_training_frame):
        """
        Constructor method jo trainmodelframe class ka instance banate waqt call hota hai.
        Parameters:
            - master: Tkinter window ya frame jisme yeh trainmodelframe attach hoga.
            - show_main_screen: Function jo main screen dikhane ke liye call hota hai.
        """
        super().__init__(mainapp)
        self.mainapp_obj = mainapp
        self.callback_main_Screen = show_main_screen
        self.show_model_training_frame = show_model_training_frame

        self.configure_gui()

    def configure_gui(self):
        """
        Yeh method GUI widgets ko create aur arrange karne ke liye use hoti hai.
        Isme buttons aur labels create aur arrange kiye jaate hain.
        """

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20, fill="x", expand=True)

        # Add another frame inside `button_frame` to center the buttons horizontally
        self.inner_frame = tk.Frame(button_frame)
        self.inner_frame.pack(expand=True)

        self.label_title = tk.Label(self.inner_frame, text="Train Model", font=("Arial", 24), pady=20)
        self.label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Button styles define karte hain
        button_style_large = {"font": ("Arial", 14), "width": 15, "height": 2, "padx": 10, "pady": 10}

        # Back button to return to the main screen
        self.back_button = tk.Button(self.inner_frame, text="Back to Main", command=self.callback_main_Screen)
        self.back_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.dataset_info_label = tk.Label(self.inner_frame, text=f"Data set with {len(self.mainapp_obj.image_paths)} images and {len(self.mainapp_obj.image_paths)} labels is ready to be Loaded")
        self.dataset_info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        # Label to show dataset information
        if len(self.mainapp_obj.image_paths) > 0:
            self.dataset_info_label = tk.Label(self.inner_frame, text="No dataset loaded")
            self.dataset_info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            return
    
        # Button to upload dataset
        self.load_dataset = tk.Button(self.inner_frame, text="Load Dataset", **button_style_large, command=self.LoadDataset)
        self.load_dataset.grid(row=3, column=0, padx=10, pady=10)

        # Button to select model
        self.start_training = tk.Button(self.inner_frame, text="Start Training", **button_style_large, command=self.show_model_training_frame)
        self.start_training.grid(row=3, column=1, padx=10, pady=10)

    def LoadDataset(self):
        LoadDataset(self)
