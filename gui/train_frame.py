import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from Implementation.backend import load_images_from_folder, augment_image
from gui.preprocessing import PreprocessingFrame
import os

class trainmodelframe(tk.Frame):
    def __init__(self, master, show_main_screen):
        """
        Constructor method jo trainmodelframe class ka instance banate waqt call hota hai.
        Parameters:
            - master: Tkinter window ya frame jisme yeh trainmodelframe attach hoga.
            - show_main_screen: Function jo main screen dikhane ke liye call hota hai.
        """
        super().__init__(master)
        self.master = master
        self.callback_main_Screen = show_main_screen

        # Initialize dataset path, image paths, and loaded images
        self.master.dataset_path = ""
        self.master.image_paths = []
        self.master.loaded_images = []
        self.create_widgets()

    def create_widgets(self):
        """
        Yeh method GUI widgets ko create aur arrange karne ke liye use hoti hai.
        Isme buttons aur labels create aur arrange kiye jaate hain.
        """
        # Back button to return to the main screen
        self.back_button = tk.Button(self, text="Back to Main", command=self.callback_main_Screen)
        self.back_button.pack()

        # Label to show dataset information
        self.dataset_info_label = tk.Label(self, text="No dataset loaded")
        self.dataset_info_label.pack()

        # Button to upload dataset
        self.upload_button = tk.Button(self, text="Upload Dataset", command=self.upload_dataset)
        self.upload_button.pack()

        # Button to preprocess data
        self.preprocess_button = tk.Button(self, text="Preprocess Data", command=self.call_preprocessingframe)
        self.preprocess_button.pack()

        # Button to augment data
        self.augment_button = tk.Button(self, text="Augment Data", command=self.augment_data)
        self.augment_button.pack()

        # Button to select model
        self.select_model_button = tk.Button(self, text="Select Model", command=self.select_model)
        self.select_model_button.pack()

    def upload_dataset(self):
        """
        Upload button click hone par call hoti hai.
        Yeh method dataset folder ko select karne ke liye dialog open karti hai aur images ko load karti hai.
        """
        self.master.dataset_path = filedialog.askdirectory(title="Select Dataset Folder")
        directory_path = self.master.dataset_path
        self.master.image_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))]
        if self.master.dataset_path:
            self.master.loaded_images = load_images_from_folder(self.master.dataset_path)
            
            # Get the number of images and update display
            num_images = len(self.master.loaded_images)
            self.dataset_info_label.config(text=f"Dataset loaded from: {self.master.dataset_path}\nNumber of images: {num_images}")
            
            # Show a message box with dataset details
            messagebox.showinfo("Dataset Uploaded", f"Dataset uploaded from: {self.master.dataset_path}\nNumber of images: {num_images}")
        else:
            messagebox.showwarning("No Dataset", "Please select a valid dataset folder.")

    def call_preprocessingframe(self):
        """
        Preprocess button click hone par call hoti hai.
        Yeh method ek new window open karti hai jahan data preprocessing ke options hote hain.
        """
        if not self.master.dataset_path:
            messagebox.showwarning("No Dataset", "Please upload a dataset first.")
            return
        
        self.preprocess_window = tk.Toplevel(self)
        self.preprocess_window.title("Data Preprocessing")
        self.preprocess_window.geometry("1200x800")
        PreprocessingFrame(self.preprocess_window, self.preprocess_window)

    def augment_data(self):
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

        self.build_augmentation_interface(augment_window)

    def build_augmentation_interface(self, augment_window):
        """
        Yeh method data augmentation ke liye GUI interface ko build karti hai.
        Isme image preview, checkboxes, buttons aur progress bar included hain.
        """
        # Image preview frame
        preview_frame = tk.Frame(augment_window)
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas and Scrollbar for image grid
        canvas = tk.Canvas(preview_frame)
        scrollbar = tk.Scrollbar(preview_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Checkboxes and image preview
        check_vars = []

        def update_grid():
            """
            Update karta hai image grid ko based on loaded images aur selection.
            """
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            max_width = 150
            max_height = 150
            cols = 4
            rows = (len(self.master.loaded_images) + cols - 1) // cols

            for i in range(rows):
                for j in range(cols):
                    idx = i * cols + j
                    if idx < len(self.master.loaded_images):
                        name, img = self.master.loaded_images[idx]

                        # Resize image for preview
                        img_preview = img.resize((max_width, max_height))
                        img_preview_tk = ImageTk.PhotoImage(img_preview)

                        # Create frame for image and checkbox
                        frame = tk.Frame(scrollable_frame, borderwidth=2, relief="solid")
                        frame.grid(row=i, column=j, padx=5, pady=5)

                        def on_image_click(event, idx=idx):
                            var, _ = check_vars[idx]
                            var.set(not var.get())

                        img_label = tk.Label(frame, image=img_preview_tk, bg="white")
                        img_label.pack(padx=5, pady=5)
                        img_label.bind("<Button-1>", on_image_click)
                        
                        # Add checkbox for image selection
                        var = tk.BooleanVar()
                        check_vars.append((var, idx))
                        checkbox = tk.Checkbutton(frame, variable=var)
                        checkbox.pack(side=tk.BOTTOM)

                        # Store image reference to prevent garbage collection
                        frame.image = img_preview_tk

        update_grid()

        def check_all():
            """
            All images ko select karta hai.
            """
            for var, _ in check_vars:
                var.set(True)

        def uncheck_all():
            """
            All images ko unselect karta hai.
            """
            for var, _ in check_vars:
                var.set(False)

        # Augmentation menu
        augmentation_menu = tk.Frame(augment_window)
        augmentation_menu.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        selectall_button = tk.Button(augmentation_menu, text="Select All", command=check_all)
        selectall_button.pack(pady=5)

        unselectall_button = tk.Button(augmentation_menu, text="Unselect All", command=uncheck_all)
        unselectall_button.pack(pady=5)

        rotation_label = tk.Label(augmentation_menu, text="Rotation Angle:")
        rotation_label.pack(pady=5)
        
        rotation_entry = tk.Entry(augmentation_menu)
        rotation_entry.pack(pady=5)
        
        def apply_rotation():
            """
            Selected images ko rotation apply karta hai based on user input.
            """
            angle = rotation_entry.get()
            try:
                angle = float(angle)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid rotation angle.")
                return
            
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.loaded_images[idx]
                    rotated_img = augment_image(img, "rotate", angle)
                    self.master.loaded_images[idx] = (name, rotated_img)
            
            update_grid()
            messagebox.showinfo("Rotation", f"Applied {angle} degrees rotation to selected images.")

        rotation_button = tk.Button(augmentation_menu, text="Apply Rotation", command=apply_rotation)
        rotation_button.pack(pady=5)

        # Presets for rotation
        presets_frame = tk.Frame(augmentation_menu)
        presets_frame.pack(pady=10)

        def apply_preset_rotation(angle):
            """
            Preset angles apply karta hai selected images ko.
            """
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.loaded_images[idx]
                    rotated_img = augment_image(img, "rotate", angle)
                    self.master.loaded_images[idx] = (name, rotated_img)
            
            update_grid()
            messagebox.showinfo("Rotation", f"Applied {angle} degrees rotation to selected images.")

        tk.Button(presets_frame, text="90 Degrees", command=lambda: apply_preset_rotation(90)).pack(side=tk.LEFT, padx=5)
        tk.Button(presets_frame, text="180 Degrees", command=lambda: apply_preset_rotation(180)).pack(side=tk.LEFT, padx=5)
        tk.Button(presets_frame, text="270 Degrees", command=lambda: apply_preset_rotation(270)).pack(side=tk.LEFT, padx=5)

        # Augmentation checkboxes
        flip_horizontal_var = tk.BooleanVar()
        flip_vertical_var = tk.BooleanVar()
        noise_var = tk.BooleanVar()
        
        tk.Checkbutton(augmentation_menu, text="Flip Horizontally", variable=flip_horizontal_var).pack(anchor="w", padx=10)
        tk.Checkbutton(augmentation_menu, text="Flip Vertically", variable=flip_vertical_var).pack(anchor="w", padx=10)
        tk.Checkbutton(augmentation_menu, text="Add Noise", variable=noise_var).pack(anchor="w", padx=10)
        
        noise_value_label = tk.Label(augmentation_menu, text="Noise Value:")
        noise_value_label.pack(pady=5)
        
        noise_value_entry = tk.Entry(augmentation_menu)
        noise_value_entry.pack(pady=5)
        
        def apply_augmentations():
            """
            Selected images par specified augmentations apply karta hai aur progress bar update karta hai.
            """
            progress_window = tk.Toplevel(augment_window)
            progress_window.title("Data Augmentation Progress")
            progress_window.geometry("600x400")
            
            tk.Label(progress_window, text="Applying augmentations...").pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=500, mode="determinate")
            progress_bar.pack(pady=10)
            progress_bar["maximum"] = len(check_vars)
            progress_bar["value"] = 0

            def run_augmentation():
                """
                Augmentation ko background thread mein run karta hai aur progress bar ko update karta hai.
                """
                for var, idx in check_vars:
                    if var.get():
                        name, img = self.master.loaded_images[idx]
                        if flip_horizontal_var.get():
                            img = augment_image(img, "flip_horizontal")
                        if flip_vertical_var.get():
                            img = augment_image(img, "flip_vertical")
                        if noise_var.get():
                            noise_value = noise_value_entry.get()
                            try:
                                noise_value = float(noise_value)
                            except ValueError:
                                messagebox.showwarning("Invalid Input", "Please enter a valid noise value.")
                                return
                            img = augment_image(img, "add_noise", noise_value)
                        # Update image list
                        self.master.loaded_images[idx] = (name, img)
                        progress_bar["value"] += 1
                        progress_window.update_idletasks()

                messagebox.showinfo("Augmentation", "Data augmentation completed!")
                progress_window.destroy()

            threading.Thread(target=run_augmentation).start()

        augment_button = tk.Button(augmentation_menu, text="Apply Augmentations", command=apply_augmentations)
        augment_button.pack(pady=10)

    def select_model(self):
        """
        Model selection button click hone par call hoti hai.
        Yeh method model selection aur training ke functionality ko integrate karne ki jagah hai.
        """
        if not self.master.dataset_path:
            messagebox.showwarning("No Dataset", "Please upload a dataset first.")
            return

        # Model selection aur training logic ko yahan integrate kiya jaayega
        messagebox.showinfo("Model Selection", "Model selection and training functionality needs to be integrated.")
