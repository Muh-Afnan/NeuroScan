import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Implementation.backend import augment_image

class AugmentFrame(tk.Frame):
    def __init__(self, master, Augmentwindow):
        super().__init__(master)
        self.augmentwindow = Augmentwindow
        self.master = master

        self.augmentwindow.grid_columnconfigure(0, weight=8)  # Left column takes 70% of space
        self.augmentwindow.grid_columnconfigure(1, weight=2)  # Right column takes 30% of space
        self.augmentwindow.grid_rowconfigure(0, weight=1)  # Row takes all available vertical space

        self.preview_frame = tk.Frame(self.augmentwindow)
        self.preview_frame.grid(row=0, column=0, sticky="nsew")

        self.menue_frame = tk.Frame(self.augmentwindow)
        self.menue_frame.grid(row=0, column=1, sticky="nsew")

        self.check_vars = []
        self.build_augmentation_interface()
        self.build_menue_frame()

    def build_augmentation_interface(self):
        self.canvas = tk.Canvas(self.preview_frame)
        self.scrollbar = tk.Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.update_grid()

    def on_frame_configure(self, event):
        """
        Updates the scroll region of the canvas whenever the size of the scrollable_frame changes.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_grid(self):
        """
        Updates the image grid based on loaded images and selection.
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
                        var, _ = self.check_vars[idx]
                        var.set(not var.get())

                    img_label = tk.Label(frame, image=img_preview_tk, bg="white")
                    img_label.pack(padx=5, pady=5)
                    img_label.bind("<Button-1>", on_image_click)

                    # Add checkbox for image selection
                    var = tk.BooleanVar()
                    self.check_vars.append((var, idx))
                    checkbox = tk.Checkbutton(frame, variable=var)
                    checkbox.pack(side=tk.BOTTOM)

                    # Store image reference to prevent garbage collection
                    frame.image = img_preview_tk

        # Update the scroll region whenever the grid is updated
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def check_all(self):
        """
        Selects all images.
        """
        for var, _ in self.check_vars:
            var.set(True)

    def uncheck_all(self):
        """
        Unselects all images.
        """
        for var, _ in self.check_vars:
            var.set(False)
    

    def build_menue_frame(self):
        """
        Build the menu frame with all augmentation options.
        """
        # Select all and unselect all buttons
        print("I am being Called")
        selectall_button = tk.Button(self.menue_frame, text="Select All", command=self.check_all)
        selectall_button.pack(pady=5)

        unselectall_button = tk.Button(self.menue_frame, text="Unselect All", command=self.uncheck_all)
        unselectall_button.pack(pady=5)

        # Rotation
        rotation_label = tk.Label(self.menue_frame, text="Rotation Angle:")
        rotation_label.pack(pady=5)
        
        rotation_entry = tk.Entry(self.menue_frame)
        rotation_entry.pack(pady=5)

        def apply_rotation():
            """
            Applies rotation to selected images based on user input.
            """
            angle = rotation_entry.get()
            try:
                angle = float(angle)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid rotation angle.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    rotated_img = augment_image(img, "rotate", angle)
                    self.master.master.loaded_images[idx] = (name, rotated_img)
            
            self.update_grid()
            messagebox.showinfo("Rotation", f"Applied {angle} degrees rotation to selected images.")

        rotation_button = tk.Button(self.menue_frame, text="Apply Rotation", command=apply_rotation)
        rotation_button.pack(pady=5)

        # Presets for rotation
        presets_frame = tk.Frame(self.menue_frame)
        presets_frame.pack(pady=10)

        def apply_preset_rotation(angle):
            """
            Applies preset rotation angles to selected images.
            """
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    rotated_img = augment_image(img, "rotate", angle)
                    self.master.master.loaded_images[idx] = (name, rotated_img)
            
            self.update_grid()
            messagebox.showinfo("Rotation", f"Applied {angle} degrees rotation to selected images.")

        tk.Button(presets_frame, text="90 Degrees", command=lambda: apply_preset_rotation(90)).pack(side=tk.LEFT, padx=5)
        tk.Button(presets_frame, text="180 Degrees", command=lambda: apply_preset_rotation(180)).pack(side=tk.LEFT, padx=5)
        tk.Button(presets_frame, text="270 Degrees", command=lambda: apply_preset_rotation(270)).pack(side=tk.LEFT, padx=5)

        # Flip
        flip_horizontal_var = tk.BooleanVar()
        flip_vertical_var = tk.BooleanVar()
        
        tk.Checkbutton(self.menue_frame, text="Flip Horizontally", variable=flip_horizontal_var).pack(anchor="w", padx=10)
        tk.Checkbutton(self.menue_frame, text="Flip Vertically", variable=flip_vertical_var).pack(anchor="w", padx=10)
        
        # Noise Value (currently not implemented)
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
            Applies translation to selected images based on user input.
            """
            translation = translation_entry.get()
            try:
                x, y = map(int, translation.split(','))
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter valid translation values.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    translated_img = augment_image(img, "translate", x, y)
                    self.master.master.loaded_images[idx] = (name, translated_img)
            
            self.update_grid()
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
            Applies scaling to selected images based on user input.
            """
            scaling_factor = scaling_entry.get()
            try:
                scaling_factor = float(scaling_factor)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid scaling factor.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    scaled_img = augment_image(img, "scale", scaling_factor)
                    self.master.master.loaded_images[idx] = (name, scaled_img)
            
            self.update_grid()
            messagebox.showinfo("Scaling", f"Applied scaling factor of {scaling_factor} to selected images.")

        scaling_button = tk.Button(self.menue_frame, text="Apply Scaling", command=apply_scaling)
        scaling_button.pack(pady=5)

        # Elastic Deformation
        elastic_deformation_label = tk.Label(self.menue_frame, text="Elastic Deformation Parameters:")
        elastic_deformation_label.pack(pady=5)
        
        elastic_deformation_entry = tk.Entry(self.menue_frame)
        elastic_deformation_entry.pack(pady=5)
        
        def apply_elastic_deformation():
            """
            Applies elastic deformation to selected images based on user input.
            """
            parameters = elastic_deformation_entry.get()
            try:
                parameters = float(parameters)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter valid elastic deformation parameters.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    deformed_img = augment_image(img, "elastic_deformation", parameters)
                    self.master.master.loaded_images[idx] = (name, deformed_img)
            
            self.update_grid()
            messagebox.showinfo("Elastic Deformation", f"Applied elastic deformation with parameters {parameters} to selected images.")

        elastic_deformation_button = tk.Button(self.menue_frame, text="Apply Elastic Deformation", command=apply_elastic_deformation)
        elastic_deformation_button.pack(pady=5)

        # Intensity Adjustment
        intensity_label = tk.Label(self.menue_frame, text="Intensity Adjustment:")
        intensity_label.pack(pady=5)
        
        intensity_entry = tk.Entry(self.menue_frame)
        intensity_entry.pack(pady=5)
        
        def apply_intensity_adjustment():
            """
            Applies intensity adjustment to selected images based on user input.
            """
            intensity = intensity_entry.get()
            try:
                intensity = float(intensity)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter valid intensity adjustment value.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    adjusted_img = augment_image(img, "intensity_adjustment", intensity)
                    self.master.master.loaded_images[idx] = (name, adjusted_img)
            
            self.update_grid()
            messagebox.showinfo("Intensity Adjustment", f"Applied intensity adjustment of {intensity} to selected images.")

        intensity_button = tk.Button(self.menue_frame, text="Apply Intensity Adjustment", command=apply_intensity_adjustment)
        intensity_button.pack(pady=5)

        # Shearing
        shearing_label = tk.Label(self.menue_frame, text="Shearing Value:")
        shearing_label.pack(pady=5)
        
        shearing_entry = tk.Entry(self.menue_frame)
        shearing_entry.pack(pady=5)
        
        def apply_shearing():
            """
            Applies shearing to selected images based on user input.
            """
            shearing_value = shearing_entry.get()
            try:
                shearing_value = float(shearing_value)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid shearing value.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    sheared_img = augment_image(img, "shear", shearing_value)
                    self.master.master.loaded_images[idx] = (name, sheared_img)
            
            self.update_grid()
            messagebox.showinfo("Shearing", f"Applied shearing value of {shearing_value} to selected images.")

        shearing_button = tk.Button(self.menue_frame, text="Apply Shearing", command=apply_shearing)
        shearing_button.pack(pady=5)

        # Random Cropping
        random_cropping_label = tk.Label(self.menue_frame, text="Random Cropping Parameters:")
        random_cropping_label.pack(pady=5)
        
        random_cropping_entry = tk.Entry(self.menue_frame)
        random_cropping_entry.pack(pady=5)
        
        def apply_random_cropping():
            """
            Applies random cropping to selected images based on user input.
            """
            parameters = random_cropping_entry.get()
            try:
                parameters = float(parameters)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter valid random cropping parameters.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    cropped_img = augment_image(img, "random_crop", parameters)
                    self.master.master.loaded_images[idx] = (name, cropped_img)
            
            self.update_grid()
            messagebox.showinfo("Random Cropping", f"Applied random cropping with parameters {parameters} to selected images.")

        random_cropping_button = tk.Button(self.menue_frame, text="Apply Random Cropping", command=apply_random_cropping)
        random_cropping_button.pack(pady=5)

        # Noise Addition
        noise_value_label = tk.Label(self.menue_frame, text="Noise Value:")
        noise_value_label.pack(pady=5)
        
        noise_value_entry = tk.Entry(self.menue_frame)
        noise_value_entry.pack(pady=5)
        
        def apply_noise():
            """
            Applies noise to selected images based on user input.
            """
            noise_value = noise_value_entry.get()
            try:
                noise_value = float(noise_value)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid noise value.")
                return
            
            for var, idx in self.check_vars:
                if var.get():
                    name, img = self.master.master.loaded_images[idx]
                    noisy_img = augment_image(img, "add_noise", noise_value)
                    self.master.master.loaded_images[idx] = (name, noisy_img)
            
            self.update_grid()
            messagebox.showinfo("Noise Addition", f"Applied noise with value {noise_value} to selected images.")

        noise_button = tk.Button(self.menue_frame, text="Apply Noise", command=apply_noise)
        noise_button.pack(pady=5)
