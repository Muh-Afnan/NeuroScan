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
    def pad_to_square_139x139(self):
        """
        Pads each image to make it 139x139 by adding padding to the width.
        """
        for i in range(len(self.main_obj.loaded_images)):
            image = self.main_obj.loaded_images[i]
            w, h = image.shape[:2]

            # Check if the image height is already 139
            if h == 139 and w == 139:
                continue  # Skip if already square

            # Calculate padding for width to reach 139x139
            delta_h = 139 - h
            top = delta_h // 2
            bottom = delta_h - top

            # Pad the image to make it square
            color = [0, 0, 0]  # Black padding
            padded_image = cv2.copyMakeBorder(image, top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=color)
            self.main_obj.loaded_images[i] = padded_image

            # Adjust labels by shifting x_center for horizontal padding
            for label in self.main_obj.labels[i]:  # Assuming labels are stored per image
                label['y_center'] += top / 139

    def normalize_images(self):
        for i in range(len(self.main_obj.loaded_images)):
            self.main_obj.loaded_images[i] = tf.convert_to_tensor(self.main_obj.loaded_images[i], dtype=tf.float32) / 255.0

    

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