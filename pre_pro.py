import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from preprocessing_logic import normalize_image, reduce_noise, skull_strip, remove_artifacts
import os

class PreprocessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Tumor Detection - Advanced Preprocessing")
        
        # Initialize variables
        self.image_paths = []  # List to store paths of images in the dataset
        self.current_image_index = 0  # Index of the currently selected image
        self.current_image = None  # Currently loaded image
        self.thumbnails = []  # List to store thumbnail images for the scrollable frame

        # Configure the grid layout for the main window
        # root.grid_rowconfigure(0, weight=1)
        # root.grid_columnconfigure(0, weight=8)
        # root.grid_columnconfigure(1, weight=2)

        self.paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create frames for the panes
        self.left_frame = tk.Frame(self.paned_window, bg="white", width=200)
        self.right_frame = tk.Frame(self.paned_window, bg="white")

        # Add frames to the PanedWindow
        self.paned_window.add(self.left_frame)
        self.paned_window.add(self.right_frame)


        # Create a frame on the left side for thumbnails
        # self.left_frame = tk.Frame(root)
        # self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')
        # self.left_frame.grid_rowconfigure(0, weight=1)
        # self.left_frame.grid_columnconfigure(0, weight=1)

        # Create a canvas and scrollbar for scrolling through thumbnails
        self.canvas = tk.Canvas(self.left_frame)
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Bind the scrollable frame to the canvas for scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Create a window on the canvas to hold the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar into the left frame
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create a frame on the right side for control buttons and settings
        # self.right_frame = tk.Frame(root)
        # self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nswe')

        # Configure rows and columns in the right frame
        # self.right_frame.grid_rowconfigure(0, weight=1)
        # for i in range(17):
        #     self.right_frame.grid_rowconfigure(i, weight=1)
        # self.right_frame.grid_columnconfigure(0, weight=1)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create a frame on the right side for control buttons and settings
        # Note: The right frame is already added to the PanedWindow
        # You should configure it directly without redefining it
        # self.configure_right_frame()

        # Button to load dataset of images
        self.load_button = tk.Button(self.right_frame, text="Load Dataset", command=self.load_dataset)
        self.load_button.grid(row=0, column=0, padx = 20, pady=10, sticky='ew')

        # Button to apply normalization to the current image
        self.norm_button = tk.Button(self.right_frame, text="Normalize Image", command=self.apply_normalization)
        self.norm_button.grid(row=3, column=0, padx = 20,pady=10, sticky='ew')

        # Controls for noise reduction
        self.noise_label = tk.Label(self.right_frame, text="Noise Reduction:")
        self.noise_label.grid(row=4, column=0, padx = 20,pady=5, sticky='w')
        self.noise_var = tk.StringVar(value='gaussian')  # Default noise reduction method
        self.noise_gaussian = tk.Radiobutton(self.right_frame, text="Gaussian", variable=self.noise_var, value='gaussian')
        self.noise_median = tk.Radiobutton(self.right_frame, text="Median", variable=self.noise_var, value='median')
        self.noise_gaussian.grid(row=5, column=0, sticky='w')
        self.noise_median.grid(row=6, column=0, sticky='w')

        # Slider to select kernel size for noise reduction
        self.kernel_size_label = tk.Label(self.right_frame, text="Kernel Size:")
        self.kernel_size_label.grid(row=7, column=0, padx = 20,pady=5, sticky='w')
        self.kernel_size_slider = tk.Scale(self.right_frame, from_=1, to=15, orient=tk.HORIZONTAL)
        self.kernel_size_slider.set(5)  # Default kernel size
        self.kernel_size_slider.grid(row=8, column=0, padx = 20,pady=5, sticky='ew')

        # Button to apply noise reduction
        self.noise_button = tk.Button(self.right_frame, text="Apply Noise Reduction", command=self.apply_noise_reduction)
        self.noise_button.grid(row=9, column=0, padx = 20,pady=10, sticky='ew')

        # Controls for skull stripping
        self.skull_label = tk.Label(self.right_frame, text="Skull Stripping Threshold:")
        self.skull_label.grid(row=10, column=0, padx = 20,pady=5, sticky='w')
        self.skull_threshold_slider = tk.Scale(self.right_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.skull_threshold_slider.set(10)  # Default threshold
        self.skull_threshold_slider.grid(row=11, column=0, padx = 20,pady=5, sticky='ew')

        # Button to apply skull stripping
        self.skull_button = tk.Button(self.right_frame, text="Apply Skull Stripping", command=self.apply_skull_stripping)
        self.skull_button.grid(row=12, column=0, padx = 20,pady=10, sticky='ew')

        # Controls for artifact removal
        self.artifact_label = tk.Label(self.right_frame, text="Artifact Removal:")
        self.artifact_label.grid(row=13, column=0, padx = 20,pady=5, sticky='w')
        self.artifact_var = tk.StringVar(value='default')  # Default artifact removal method
        self.artifact_default = tk.Radiobutton(self.right_frame, text="Default", variable=self.artifact_var, value='default')
        self.artifact_custom = tk.Radiobutton(self.right_frame, text="Custom", variable=self.artifact_var, value='custom')
        self.artifact_default.grid(row=14, column=0, sticky='w')
        self.artifact_custom.grid(row=15, column=0, sticky='w')

        # Button to apply artifact removal
        self.artifact_button = tk.Button(self.right_frame, text="Remove Artifacts", command=self.apply_artifact_removal)
        self.artifact_button.grid(row=16, column=0, padx = 20,pady=10, sticky='ew')

        # Progress bar to show ongoing processes
        self.progress_bar = ttk.Progressbar(self.right_frame, orient="horizontal", mode="indeterminate")
        self.progress_bar.grid(row=17, column=0, padx = 20,pady=10, sticky='ew')

    def load_dataset(self):
        # Opens a file dialog to select a directory and loads image file paths
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.image_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))]
            if self.image_paths:
                self.current_image_index = 0
                self.display_thumbnails()  # Show image thumbnails in the left frame
                self.load_image(self.image_paths[self.current_image_index])  # Load the first image
            else:
                messagebox.showwarning("No Images Found", "No images found in the selected directory.")

    def display_thumbnails(self):
        # Clears existing thumbnails from the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.thumbnails = []  # Reset thumbnails list
        for idx, image_path in enumerate(self.image_paths):
            image = cv2.imread(image_path)  # Read image file
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB format
            image_pil = Image.fromarray(image_rgb)  # Convert to PIL image
            image_pil.thumbnail((100, 100))  # Resize for thumbnails
            image_tk = ImageTk.PhotoImage(image_pil)  # Convert to Tkinter image format
            self.thumbnails.append(image_tk)

            # Create a button with the thumbnail image
            button = tk.Button(self.scrollable_frame, image=image_tk, command=lambda idx=idx: self.load_image(self.image_paths[idx]))
            button.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)  # Arrange thumbnails in a grid

    def load_image(self, image_path):
        # Load and display the selected image
        self.current_image = cv2.imread(image_path)
        self.display_image(self.current_image)  # Display the image in the right frame

    def display_image(self, image):
        # Display the current image in the scrollable frame
        if image is None:
            return
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB format
        image_pil = Image.fromarray(image_rgb)  # Convert to PIL image
        image_pil.thumbnail((100, 100))  # Resize for thumbnails
        image_tk = ImageTk.PhotoImage(image_pil)  # Convert to Tkinter image format

                # Check if thumbnail already exists
        if 0 <= self.current_image_index < len(self.thumbnails):
            # Replace existing thumbnail with updated image
            self.thumbnails[self.current_image_index] = image_tk
            # Update or add a new button for the thumbnail
            button = tk.Button(self.scrollable_frame, image=image_tk, command=lambda idx=self.current_image_index: self.load_image(self.image_paths[idx]))
            button.grid(row=self.current_image_index // 4, column=self.current_image_index % 4, padx=5, pady=5)
        else:
            # Create a new button with the thumbnail image
            button = tk.Button(self.scrollable_frame, image=image_tk, command=lambda idx=self.current_image_index: self.load_image(self.image_paths[idx]))
            button.grid(row=len(self.thumbnails) // 4, column=len(self.thumbnails) % 4, padx=5, pady=5)
            self.thumbnails.append(image_tk)

    def apply_normalization(self):
        # Apply normalization to the current image and update the display
        if self.current_image is not None:
            self.progress_bar.start()  # Start the progress bar animation
            self.root.update_idletasks()  # Update the GUI to show progress bar
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
            self.root.update_idletasks()  # Update the GUI to show progress bar
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
            self.root.update_idletasks()  # Update the GUI to show progress bar
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
            self.root.update_idletasks()  # Update the GUI to show progress bar
            method = self.artifact_var.get()  # Get the selected artifact removal method
            artifact_removed_image = remove_artifacts(self.current_image, method)
            self.display_image(artifact_removed_image)  # Display the artifact-removed image
            self.progress_bar.stop()  # Stop the progress bar animation
            messagebox.showinfo("Success", "Artifact removal applied successfully!")
        else:
            messagebox.showerror("Error", "No image loaded!")

if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    # Initialize the application
    app = PreprocessingApp(root)
    # Start the Tkinter main loop
    root.mainloop()

