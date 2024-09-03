import tkinter as tk
from tkinter import ttk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from Implementation.backend import load_images_from_folder,augment_image
from gui.preprocessing import PreprocessingFrame
import os

class trainmodelframe(tk.Frame):
    def __init__(self, master ,show_main_screen):
        super().__init__(master)
        self.master = master
        self.callback_main_Screen = show_main_screen

    

        self.master.dataset_path = ""
        self.master.image_paths = []
        self.master.loaded_images = []
        self.create_widgets()
 

    def create_widgets(self):
        self.back_button= tk.Button(self, text="Back to Main", command=self.callback_main_Screen)
        self.back_button.pack()

        self.dataset_info_label = tk.Label(self, text="No dataset loaded")
        self.dataset_info_label.pack()

        self.upload_button = tk.Button(self, text="Upload Dataset", command=self.upload_dataset)
        self.upload_button.pack()

            
        self.preprocess_button = tk.Button(self, text="Preprocess Data", command=self.call_preprocessingframe)
        self.preprocess_button.pack()

        self.augment_button = tk.Button(self, text="Augment Data", command=self.augment_data)
        self.augment_button.pack()

        self.select_model_button = tk.Button(self, text="Select Model", command=self.select_model)
        self.select_model_button.pack()    

    def upload_dataset(self):
        self.master.dataset_path = filedialog.askdirectory(title="Select Dataset Folder")
        directory_path = self.master.dataset_path
        self.master.image_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))]
        if self.master.dataset_path:
            self.master.loaded_images = load_images_from_folder(self.master.dataset_path)
            
            # Get the number of images
            num_images = len(self.master.loaded_images)
            
            # Update the display with dataset information
            self.dataset_info_label.config(text=f"Dataset loaded from: {self.master.dataset_path}\nNumber of images: {num_images}")
            
            # Show a message box with the details
            messagebox.showinfo("Dataset Uploaded", f"Dataset uploaded from: {self.master.dataset_path}\nNumber of images: {num_images}")
        else:
            messagebox.showwarning("No Dataset", "Please select a valid dataset folder.")


    def call_preprocessingframe(self, master):
        if not self.master.dataset_path:
            messagebox.showwarning("No Dataset", "Please upload a dataset first.")
            return
        
        self.preprocess_window = tk.Toplevel(self)
        self.preprocess_window.title("Data Preprocessing")
        self.preprocess_window.geometry("1200x800")
        PreprocessingFrame(self, self.preprocess_window,master)
        
    def augment_data(self):
        if not self.master.dataset_path:
            messagebox.showwarning("No Dataset", "Please upload a dataset first.")
            return

        augment_window = tk.Toplevel(self)
        augment_window.title("Data Augmentation")
        augment_window.geometry("1200x800")

        self.build_augmentation_interface(augment_window)

    def build_augmentation_interface(self, augment_window):
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
                            # event.widget.config(bg="lightblue" if var.get() else "white")

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
            for aa in check_vars:
                var, _ = aa
                var.set(True)

        def uncheck_all():
            for aa in check_vars:
                var, _ = aa
                var.set(False)

        # Augmentation menu
        augmentation_menu = tk.Frame(augment_window)
        augmentation_menu.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)


        selectall_button = tk.Button(augmentation_menu, text="Select All", command=check_all)
        selectall_button.pack(pady=5)

        unselectall_button = tk.Button(augmentation_menu, text="Un Select All", command=uncheck_all)
        unselectall_button.pack(pady=5)

        rotation_label = tk.Label(augmentation_menu, text="Rotation Angle:")
        rotation_label.pack(pady=5)
        
        rotation_entry = tk.Entry(augmentation_menu)
        rotation_entry.pack(pady=5)
        
        def apply_rotation():
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
            # augmentation_menu.focus()

        rotation_button = tk.Button(augmentation_menu, text="Apply Rotation", command=apply_rotation)
        rotation_button.pack(pady=5)

        # Presets for rotation
        presets_frame = tk.Frame(augmentation_menu)
        presets_frame.pack(pady=10)

        def apply_preset_rotation(angle):
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
            progress_window = tk.Toplevel(augment_window)
            progress_window.title("Data Augmentation Progress")
            progress_window.geometry("600x400")
            
            tk.Label(progress_window, text="Applying augmentations...").pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=500, mode="determinate")
            progress_bar.pack(pady=10)
            progress_bar["maximum"] = len(check_vars)
            progress_bar["value"] = 0

            def run_augmentation():
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
        if not self.master.dataset_path:
            messagebox.showwarning("No Dataset", "Please upload a dataset first.")
            return

        # Here you would integrate model selection and training logic
        messagebox.showinfo("Model Selection", "Model selection and training functionality needs to be integrated.")