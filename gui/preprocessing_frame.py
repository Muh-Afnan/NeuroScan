import tkinter as tk
from tkinter import ttk
import tensorflow as tf
from Implementation.preprocessing_data import resize_data,normalize_data
import cv2 as cv2

class PreprocessingFrame(tk.Frame):
    def __init__(self, train_frame, mainapp_obj):
        super().__init__(train_frame)
        self.train_frame = train_frame
        self.main_obj = mainapp_obj


        self.create_interface()

    def create_interface(self):
        self.second_window = tk.Toplevel(self)
        self.second_window.title("Data Preprocessing Progress")
        self.second_window.geometry("800x500")
        
        # self.progress_bar = ttk.Progressbar(self.second_window, orient="horizontal", length = 200, mode="indeterminate", variable=progress_var)
        
        self.inner_frame = tk.Frame(self.second_window)
        self.inner_frame.pack()
    
    # def load_tf_image(image)
    #     image = tf.io.read_file(path) 
    
    def load_images(self):
        """
        Loads images from the specified paths and appends them to loaded_images as NumPy arrays.
        Raises an error if an image cannot be loaded.
        """
        for path in self.main_obj.image_paths:
            image = cv2.imread(path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Image at path {path} could not be loaded")
            self.main_obj.loaded_images.append(image)

    def remove_noise(self, filter_strength=10, template_window_size=7, search_window_size=21):
        """
        Removes noise from images using OpenCV's fastNlMeansDenoising.
        Supports both color and grayscale images.
        """
        for i in range(len(self.main_obj.loaded_images)):
            if len(self.main_obj.loaded_images[i].shape) == 3:  # Color image
                self.main_obj.loaded_images[i] = cv2.fastNlMeansDenoisingColored(
                    self.main_obj.loaded_images[i], None, filter_strength, filter_strength,
                    template_window_size, search_window_size
                )
            else:  # Grayscale image
                self.main_obj.loaded_images[i] = cv2.fastNlMeansDenoising(
                    self.main_obj.loaded_images[i], None, filter_strength, 
                    template_window_size, search_window_size
                )

    def std_resize_images(self, target_height=256, target_width=256):
        """
        Resizes images using OpenCV to the target dimensions.
        """
        for i in range(len(self.main_obj.loaded_images)):
            # Resize with OpenCV and keep as NumPy array
            self.main_obj.loaded_images[i] = cv2.resize(
                self.main_obj.loaded_images[i], (target_width, target_height), interpolation=cv2.INTER_AREA
            )

    def normalize_images(self):
        """
        Normalizes images by scaling pixel values to [0, 1] and converts them to TensorFlow tensors.
        """
        for i in range(len(self.main_obj.loaded_images)):
            # Convert to TensorFlow tensor and normalize
            image_tensor = tf.convert_to_tensor(self.main_obj.loaded_images[i], dtype=tf.float32) / 255.0
            self.main_obj.loaded_images[i] = image_tensor

    def convert_to_dataset(self):
        """
        Converts the loaded images into a TensorFlow Dataset.
        """
        dataset = tf.data.Dataset.from_tensor_slices(self.main_obj.loaded_images)
        return dataset


        

        # button_style_large = {"font": ("Arial", 14), "width": 15, "height": 2, "padx": 10, "pady": 10}

        # self.resize_button = tk.Button(self.inner_frame, text="Resize Data Set", **button_style_large, command = self.resize_data)
        # self.resize_button.grid(row=0, column=0,padx=10, pady=10)

        # self.normalize_data = tk.Button(self.inner_frame, text="Normalize Data Set", **button_style_large, command = self.normalize_data)
        # self.normalize_data.grid(row=0, column=1,padx=10, pady=10)