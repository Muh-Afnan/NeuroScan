import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
from Implementation.backend import augment_image
class AugmentFrame(tk.Frame):
    def __init__(self, master, Augmentwindow):
        super().__init__(master)
        self.augmentwindow = Augmentwindow
        self.master = master
        
        self.preview_frame = tk.Frame(self.augmentwindow )
        self.preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.menue_frame = tk.Frame(self.augmentwindow )
        self.menue_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True, padx=10, pady=10)
        self.check_vars = []
        self.build_augmentation_interface()

    def build_augmentation_interface(self):
        self.canvas = tk.Canvas(self.preview_frame)
        self.scrollbar = tk.Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        # self.scrollable_frame.bind(
        #     "<Configure>",
        #     lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # )
        def on_frame_configure(event):
            # Update the scroll region of the canvas
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", on_frame_configure)

        # Checkboxes and image preview
        check_vars = []

        def update_grid():
            """
            Update karta hai image grid ko based on loaded images aur selection.
            """
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            max_width = 150
            max_height = 150
            cols = 4
            rows = (len(self.master.master.loaded_images) + cols - 1) // cols

            for i in range(rows):
                for j in range(cols):
                    idx = i * cols + j
                    if idx < len(self.master.master.loaded_images):
                        name, img = self.master.master.loaded_images[idx]

                        # Resize image for preview
                        img_preview = img.resize((max_width, max_height))
                        img_preview_tk = ImageTk.PhotoImage(img_preview)

                        # Create frame for image and checkbox
                        frame = tk.Frame(self.scrollable_frame, borderwidth=2, relief="solid")
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
        # self.menue_frame = tk.Frame(self.augmentwindow)
        # self.menue_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        

        selectall_button = tk.Button(self.menue_frame, text="Select All", command=check_all)
        selectall_button.pack(pady=5)

        unselectall_button = tk.Button(self.menue_frame, text="Unselect All", command=uncheck_all)
        unselectall_button.pack(pady=5)

        # Rotation
        rotation_label = tk.Label(self.menue_frame, text="Rotation Angle:")
        rotation_label.pack(pady=5)
        
        rotation_entry = tk.Entry(self.menue_frame)
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
                    name, img = self.master.master.loaded_images[idx]
                    rotated_img = augment_image(img, "rotate", angle)
                    self.master.master.loaded_images[idx] = (name, rotated_img)
            
            update_grid()
            messagebox.showinfo("Rotation", f"Applied {angle} degrees rotation to selected images.")

        rotation_button = tk.Button(self.menue_frame, text="Apply Rotation", command=apply_rotation)
        rotation_button.pack(pady=5)

        # Presets for rotation
        presets_frame = tk.Frame(self.menue_frame)
        presets_frame.pack(pady=10)

        def apply_preset_rotation(angle):
            """
            Preset angles apply karta hai selected images ko.
            """
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    rotated_img = augment_image(img, "rotate", angle)
                    self.master.master.loaded_images[idx] = (name, rotated_img)
            
            update_grid()
            messagebox.showinfo("Rotation", f"Applied {angle} degrees rotation to selected images.")

        tk.Button(presets_frame, text="90 Degrees", command=lambda: apply_preset_rotation(90)).pack(side=tk.LEFT, padx=5)
        tk.Button(presets_frame, text="180 Degrees", command=lambda: apply_preset_rotation(180)).pack(side=tk.LEFT, padx=5)
        tk.Button(presets_frame, text="270 Degrees", command=lambda: apply_preset_rotation(270)).pack(side=tk.LEFT, padx=5)

        # Flip
        flip_horizontal_var = tk.BooleanVar()
        flip_vertical_var = tk.BooleanVar()
        noise_var = tk.BooleanVar()
        
        tk.Checkbutton(self.menue_frame, text="Flip Horizontally", variable=flip_horizontal_var).pack(anchor="w", padx=10)
        tk.Checkbutton(self.menue_frame, text="Flip Vertically", variable=flip_vertical_var).pack(anchor="w", padx=10)
        tk.Checkbutton(self.menue_frame, text="Add Noise", variable=noise_var).pack(anchor="w", padx=10)
        
        noise_value_label = tk.Label(self.menue_frame, text="Noise Value:")
        noise_value_label.pack(pady=5)
        
        noise_value_entry = tk.Entry(self.menue_frame)
        noise_value_entry.pack(pady=5)
        
        # Translation
        translation_label = tk.Label(self.menue_frame, text="Translation (x, y):")
        translation_label.pack(pady=5)
        
        translation_entry = tk.Entry(self.menue_frame)
        translation_entry.pack(pady=5)
        
        def apply_translation():
            """
            Selected images ko translation apply karta hai based on user input.
            """
            translation = translation_entry.get()
            try:
                x, y = map(int, translation.split(','))
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter valid translation values.")
                return
            
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    translated_img = augment_image(img, "translate", x, y)
                    self.master.master.loaded_images[idx] = (name, translated_img)
            
            update_grid()
            messagebox.showinfo("Translation", f"Applied translation (x={x}, y={y}) to selected images.")

        translation_button = tk.Button(self.menue_frame, text="Apply Translation", command=apply_translation)
        translation_button.pack(pady=5)

        # Scaling
        scaling_label = tk.Label(self.menue_frame, text="Scaling Factor:")
        scaling_label.pack(pady=5)
        
        scaling_entry = tk.Entry(self.menue_frame)
        scaling_entry.pack(pady=5)
        
        def apply_scaling():
            """
            Selected images ko scaling apply karta hai based on user input.
            """
            scaling_factor = scaling_entry.get()
            try:
                scaling_factor = float(scaling_factor)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid scaling factor.")
                return
            
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    scaled_img = augment_image(img, "scale", scaling_factor)
                    self.master.master.loaded_images[idx] = (name, scaled_img)
            
            update_grid()
            messagebox.showinfo("Scaling", f"Applied scaling factor of {scaling_factor} to selected images.")

        scaling_button = tk.Button(self.menue_frame, text="Apply Scaling", command=apply_scaling)
        scaling_button.pack(pady=5)

        # Elastic Deformation
        elastic_deformation_label = tk.Label(self.menue_frame, text="Elastic Deformation Parameters:")
        elastic_deformation_label.pack(pady=5)

        def apply_elastic_deformation():
            """
            Selected images ko elastic deformation apply karta hai.
            """
            # This needs specific implementation details
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    deformed_img = augment_image(img, "elastic_deformation")
                    self.master.master.loaded_images[idx] = (name, deformed_img)
            
            update_grid()
            messagebox.showinfo("Elastic Deformation", "Applied elastic deformation to selected images.")

        elastic_deformation_button = tk.Button(self.menue_frame, text="Apply Elastic Deformation", command=apply_elastic_deformation)
        elastic_deformation_button.pack(pady=5)

        # Intensity Adjustment
        intensity_label = tk
            # Intensity Adjustment
        intensity_label = tk.Label(self.menue_frame, text="Intensity Adjustment Factor:")
        intensity_label.pack(pady=5)

        intensity_entry = tk.Entry(self.menue_frame)
        intensity_entry.pack(pady=5)

        def apply_intensity_adjustment():
            """
            Selected images ko intensity adjustment apply karta hai based on user input.
            """
            factor = intensity_entry.get()
            try:
                factor = float(factor)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid intensity adjustment factor.")
                return
            
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    adjusted_img = augment_image(img, "intensity", factor)
                    self.master.loaded_images[idx] = (name, adjusted_img)
            
            update_grid()
            messagebox.showinfo("Intensity Adjustment", f"Applied intensity adjustment factor of {factor} to selected images.")

        intensity_button = tk.Button(self.menue_frame, text="Apply Intensity Adjustment", command=apply_intensity_adjustment)
        intensity_button.pack(pady=5)

        # Shearing
        shearing_label = tk.Label(self.menue_frame, text="Shearing Factor:")
        shearing_label.pack(pady=5)
        
        shearing_entry = tk.Entry(self.menue_frame)
        shearing_entry.pack(pady=5)
        
        def apply_shearing():
            """
            Selected images ko shearing apply karta hai based on user input.
            """
            factor = shearing_entry.get()
            try:
                factor = float(factor)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid shearing factor.")
                return
            
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    sheared_img = augment_image(img, "shear", factor)
                    self.master.master.loaded_images[idx] = (name, sheared_img)
            
            update_grid()
            messagebox.showinfo("Shearing", f"Applied shearing factor of {factor} to selected images.")

        shearing_button = tk.Button(self.menue_frame, text="Apply Shearing", command=apply_shearing)
        shearing_button.pack(pady=5)

        # Random Cropping
        crop_label = tk.Label(self.menue_frame, text="Crop Size (width, height):")
        crop_label.pack(pady=5)
        
        crop_entry = tk.Entry(self.menue_frame)
        crop_entry.pack(pady=5)
        
        def apply_random_cropping():
            """
            Selected images ko random cropping apply karta hai based on user input.
            """
            size = crop_entry.get()
            try:
                width, height = map(int, size.split(','))
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter valid crop dimensions.")
                return
            
            for var, idx in check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    cropped_img = augment_image(img, "crop", width, height)
                    self.master.master.loaded_images[idx] = (name, cropped_img)
            
            update_grid()
            messagebox.showinfo("Random Cropping", f"Applied random cropping with size (width={width}, height={height}) to selected images.")

        crop_button = tk.Button(self.menue_frame, text="Apply Random Cropping", command=apply_random_cropping)
        crop_button.pack(pady=5)