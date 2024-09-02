import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from preprocessing_logic import normalize_image, reduce_noise, skull_strip, remove_artifacts

class PreprocessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Tumor Detection - Advanced Preprocessing")
        self.image_path = None
        self.image = None

        # Left frame for image display
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        # Right frame for controls
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # Load Image Button
        self.load_button = tk.Button(self.right_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, pady=10)

        # Normalization Button
        self.norm_button = tk.Button(self.right_frame, text="Normalize Image", command=self.apply_normalization)
        self.norm_button.grid(row=1, column=0, pady=10)

        # Noise Reduction Controls
        self.noise_label = tk.Label(self.right_frame, text="Noise Reduction:")
        self.noise_label.grid(row=2, column=0, pady=5)
        self.noise_var = tk.StringVar(value='gaussian')
        self.noise_gaussian = tk.Radiobutton(self.right_frame, text="Gaussian", variable=self.noise_var, value='gaussian')
        self.noise_median = tk.Radiobutton(self.right_frame, text="Median", variable=self.noise_var, value='median')
        self.noise_gaussian.grid(row=3, column=0)
        self.noise_median.grid(row=4, column=0)

        self.kernel_size_label = tk.Label(self.right_frame, text="Kernel Size:")
        self.kernel_size_label.grid(row=5, column=0, pady=5)
        self.kernel_size_slider = tk.Scale(self.right_frame, from_=1, to=15, orient=tk.HORIZONTAL)
        self.kernel_size_slider.set(5)
        self.kernel_size_slider.grid(row=6, column=0, pady=5)

        self.noise_button = tk.Button(self.right_frame, text="Apply Noise Reduction", command=self.apply_noise_reduction)
        self.noise_button.grid(row=7, column=0, pady=10)

        # Skull Stripping Controls
        self.skull_label = tk.Label(self.right_frame, text="Skull Stripping Threshold:")
        self.skull_label.grid(row=8, column=0, pady=5)
        self.skull_threshold_slider = tk.Scale(self.right_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.skull_threshold_slider.set(10)
        self.skull_threshold_slider.grid(row=9, column=0, pady=5)

        self.skull_button = tk.Button(self.right_frame, text="Apply Skull Stripping", command=self.apply_skull_stripping)
        self.skull_button.grid(row=10, column=0, pady=10)

        # Artifact Removal Controls
        self.artifact_label = tk.Label(self.right_frame, text="Artifact Removal:")
        self.artifact_label.grid(row=11, column=0, pady=5)
        self.artifact_var = tk.StringVar(value='default')
        self.artifact_default = tk.Radiobutton(self.right_frame, text="Default", variable=self.artifact_var, value='default')
        self.artifact_custom = tk.Radiobutton(self.right_frame, text="Custom", variable=self.artifact_var, value='custom')
        self.artifact_default.grid(row=12, column=0)
        self.artifact_custom.grid(row=13, column=0)

        self.artifact_button = tk.Button(self.right_frame, text="Remove Artifacts", command=self.apply_artifact_removal)
        self.artifact_button.grid(row=14, column=0, pady=10)

        # Canvas to Display Images
        self.canvas = tk.Canvas(self.left_frame, width=500, height=500)
        self.canvas.pack()

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.display_image(self.image)

    def display_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil.thumbnail((500, 500))  # Resize for the canvas
        image_tk = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(250, 250, image=image_tk)
        self.canvas.image = image_tk

    def apply_normalization(self):
        if self.image is not None:
            norm_image = normalize_image(self.image)
            norm_image = (norm_image * 255).astype(np.uint8)
            self.display_image(norm_image)
        else:
            messagebox.showerror("Error", "No image loaded!")

    def apply_noise_reduction(self):
        if self.image is not None:
            method = self.noise_var.get()
            kernel_size = self.kernel_size_slider.get()
            if kernel_size % 2 == 0:
                kernel_size += 1  # Ensure kernel size is odd for Gaussian and median blur
            noise_reduced_image = reduce_noise(self.image, method, kernel_size)
            self.display_image(noise_reduced_image)
        else:
            messagebox.showerror("Error", "No image loaded!")

    def apply_skull_stripping(self):
        if self.image is not None:
            threshold = self.skull_threshold_slider.get()
            skull_stripped_image = skull_strip(self.image, threshold)
            self.display_image(skull_stripped_image)
        else:
            messagebox.showerror("Error", "No image loaded!")

    def apply_artifact_removal(self):
        if self.image is not None:
            method = self.artifact_var.get()
            artifact_removed_image = remove_artifacts(self.image, method)
            self.display_image(artifact_removed_image)
        else:
            messagebox.showerror("Error", "No image loaded!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PreprocessingApp(root)
    root.mainloop()
