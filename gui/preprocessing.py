import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from Implementation.preprocessing_logic import normalize_image, reduce_noise, skull_strip, remove_artifacts
import os

class PreprocessingFrame(tk.Frame):
    def __init__(self, master,preprocess_window,master_master):
        super().__init__(master)
        self.master = master
        self.master_master = master_master
        self.preprocess_window = preprocess_window

        self.master.master.dataset_path = ""
        self.master.master.image_paths = []
        self.master.master.loaded_images = []

        self.master.create_widgets()

        self.preview_frame = tk.Frame(self.preprocess_window )
        self.preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.menue_frame = tk.Frame(self.preprocess_window )
        self.menue_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True, padx=10, pady=10)
        self.check_vars = []
        self.build_preprocessing_screen()

    def build_preprocessing_screen(self):
        self.canvas = tk.Canvas(self.preview_frame)
        self.scrollbar = tk.Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Pack Scrollbar and Canvas
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create window on Canvas to contain scrollable_frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the Configure event to update scroll region
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        
        # Set scrollbar command to the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        selectall_button = tk.Button(self.menue_frame, text="Select All", command=self.check_all)
        selectall_button.pack(pady=5)

        unselectall_button = tk.Button(self.menue_frame, text="Un Select All", command=self.uncheck_all)
        unselectall_button.pack(pady=5)

        self.norm_button = tk.Button(self.menue_frame, text="Normalize Image", command=self.apply_normalization)
        self.norm_button.pack(pady=5)

        # Controls for noise reduction
        self.noise_label = tk.Label(self.menue_frame, text="Noise Reduction:")
        self.noise_label.pack(pady=5)
        self.noise_var = tk.StringVar(value='gaussian')  # Default noise reduction method
        self.noise_gaussian = tk.Radiobutton(self.menue_frame, text="Gaussian", variable=self.noise_var, value='gaussian')
        self.noise_median = tk.Radiobutton(self.menue_frame, text="Median", variable=self.noise_var, value='median')
        self.noise_gaussian.pack(pady=5)
        self.noise_median.pack(pady=5)

        # Slider to select kernel size for noise reduction
        self.kernel_size_label = tk.Label(self.menue_frame, text="Kernel Size:")
        self.kernel_size_label.pack(pady=5)
        self.kernel_size_slider = tk.Scale(self.menue_frame, from_=1, to=15, orient=tk.HORIZONTAL)
        self.kernel_size_slider.set(5)  # Default kernel size
        self.kernel_size_slider.pack(pady=5)

        # Button to apply noise reduction
        self.noise_button = tk.Button(self.menue_frame, text="Apply Noise Reduction", command=self.apply_noise_reduction)
        self.noise_button.pack(pady=5)

        # Controls for skull stripping
        self.skull_label = tk.Label(self.menue_frame, text="Skull Stripping Threshold:")
        self.skull_label.pack(pady=5)
        self.skull_threshold_slider = tk.Scale(self.menue_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.skull_threshold_slider.set(10)  # Default threshold
        self.skull_threshold_slider.pack(pady=5)

        # Button to apply skull stripping
        self.skull_button = tk.Button(self.menue_frame, text="Apply Skull Stripping", command=self.apply_skull_stripping)
        self.skull_button.pack(pady=5)

        # Controls for artifact removal
        self.artifact_label = tk.Label(self.menue_frame, text="Artifact Removal:")
        self.artifact_label.pack(pady=5)
        self.artifact_var = tk.StringVar(value='default')  # Default artifact removal method
        self.artifact_default = tk.Radiobutton(self.menue_frame, text="Default", variable=self.artifact_var, value='default')
        self.artifact_custom = tk.Radiobutton(self.menue_frame, text="Custom", variable=self.artifact_var, value='custom')
        self.artifact_default.pack(pady=5)
        self.artifact_custom.pack(pady=5)

        # Button to apply artifact removal
        self.artifact_button = tk.Button(self.menue_frame, text="Remove Artifacts", command=self.apply_artifact_removal)
        self.artifact_button.pack(pady=5)

    def on_frame_configure(self, event):
        # Update the scroll region of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def check_all(self):
        for aa in self.check_vars:
            var, _ = aa
            var.set(True)

    def uncheck_all(self):
        for aa in self.check_vars:
            var, _ = aa
            var.set(False)
    
    def update_grid(self):
        # Clear existing widgets
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

                    img_preview = img.resize((max_width, max_height))
                    img_preview_tk = ImageTk.PhotoImage(img_preview)

                    frame = tk.Frame(self.scrollable_frame, borderwidth=2, relief="solid")
                    frame.grid(row=i, column=j, padx=5, pady=5)

                    def on_image_click(event, idx=idx):
                        var, _ = self.check_vars[idx]
                        var.set(not var.get())

                    img_label = tk.Label(frame, image=img_preview_tk, bg="white")
                    img_label.pack(padx=5, pady=5)
                    img_label.bind("<Button-1>", on_image_click)

                    var = tk.BooleanVar()
                    self.check_vars.append((var, idx))
                    checkbox = tk.Checkbutton(frame, variable=var)
                    checkbox.pack(side=tk.BOTTOM)

                    frame.image = img_preview_tk  # Store reference to avoid garbage collection

    def apply_normalization(self):
        # Apply normalization to the current image and update the display
        if self.current_image is not None:
            self.progress_bar.start()  # Start the progress bar animation
            self.update_idletasks()  # Update the GUI to show progress bar
            # Normalize the image and convert it back to 8-bit format
            norm_image = normalize_image(self.current_image)
            norm_image = (norm_image * 255).astype(np.uint8)
            self.display_image(norm_image)  # Display the normalized image
            self.progress_bar.stop()  # Stop the progress bar animation
            messagebox.showinfo("Success", "Normalization applied successfully!")
        else:
            messagebox.showerror("Error", "No image loaded!")

    def apply_noise_reduction(self):
        # Apply noise reduction to the current image and update the display
        if self.current_image is not None:
            self.progress_bar.start()  # Start the progress bar animation
            self.update_idletasks()  # Update the GUI to show progress bar
            method = self.noise_var.get()  # Get the selected noise reduction method
            kernel_size = self.kernel_size_slider.get()  # Get the selected kernel size
            if kernel_size % 2 == 0:
                kernel_size += 1  # Ensure kernel size is odd for Gaussian and median blur
            noise_reduced_image = reduce_noise(self.current_image, method, kernel_size)
            self.display_image(noise_reduced_image)  # Display the noise-reduced image
            self.progress_bar.stop()  # Stop the progress bar animation
            messagebox.showinfo("Success", "Noise reduction applied successfully!")
        else:
            messagebox.showerror("Error", "No image loaded!")

    def apply_skull_stripping(self):
        # Apply skull stripping to the current image and update the display
        if self.current_image is not None:
            self.progress_bar.start()  # Start the progress bar animation
            self.update_idletasks()  # Update the GUI to show progress bar
            threshold = self.skull_threshold_slider.get()  # Get the selected threshold value
            skull_stripped_image = skull_strip(self.current_image, threshold)
            self.display_image(skull_stripped_image)  # Display the skull-stripped image
            self.progress_bar.stop()  # Stop the progress bar animation
            messagebox.showinfo("Success", "Skull stripping applied successfully!")
        else:
            messagebox.showerror("Error", "No image loaded!")

    def apply_artifact_removal(self):
        # Apply artifact removal to the current image and update the display
        if self.current_image is not None:
            self.progress_bar.start()  # Start the progress bar animation
            self.update_idletasks()  # Update the GUI to show progress bar
            method = self.artifact_var.get()  # Get the selected artifact removal method
            artifact_removed_image = remove_artifacts(self.current_image, method)
            self.display_image(artifact_removed_image)  # Display the artifact-removed image
            self.progress_bar.stop()  # Stop the progress bar animation
            messagebox.showinfo("Success", "Artifact removal applied successfully!")
        else:
            messagebox.showerror("Error", "No image loaded!")