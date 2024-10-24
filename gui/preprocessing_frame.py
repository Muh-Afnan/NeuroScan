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
    
    def load_image(self):
        for path in self.main_obj.image_paths:
            image = cv2.imread(path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError (f"Image at Path {path} couldnot be loaded")
            self.main_obj.loaded_images.append(image)

    def std_resize_images(self):
        target_width = 256
        target_height = 256
        for i in range(len(self.main_obj.loaded_images)):
            self.main_obj.loaded_images[i] = tf.image.resize_with_pad(self.main_obj.loaded_images[i], target_height=256, target_width=256)
    
    def normalize_images(self):
        """
        This function normalizes the images in the loaded_images array.
        The pixel values are scaled to the range [0, 1].
        """
        for i in range(len(self.main_obj.loaded_images)):
            # Normalize the image by dividing by 255.0
            self.main_obj.loaded_images[i] = tf.cast(self.main_obj.loaded_images[i], tf.float32) / 255.0

    def remove_noise(image, filter_strength=10, template_window_size=7, search_window_size=21):
        
        if image is None:
            raise ValueError("Input image is None")

        # Check if the image is colored or grayscale
        if len(image.shape) == 3:
            # Colored image (MRI or CT scan in RGB)
            denoised_image = cv2.fastNlMeansDenoisingColored(image, None, filter_strength, filter_strength,
                                                            template_window_size, search_window_size)
        else:
            # Grayscale image
            denoised_image = cv2.fastNlMeansDenoising(image, None, filter_strength, 
                                                    template_window_size, search_window_size)

        return denoised_image

            # Example usage:
            # img = cv2.imread('scan_image.png')
            # denoised_img = remove_noise(img)
            # cv2.imshow('Denoised Image', denoised_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()


        

        # button_style_large = {"font": ("Arial", 14), "width": 15, "height": 2, "padx": 10, "pady": 10}

        # self.resize_button = tk.Button(self.inner_frame, text="Resize Data Set", **button_style_large, command = self.resize_data)
        # self.resize_button.grid(row=0, column=0,padx=10, pady=10)

        # self.normalize_data = tk.Button(self.inner_frame, text="Normalize Data Set", **button_style_large, command = self.normalize_data)
        # self.normalize_data.grid(row=0, column=1,padx=10, pady=10)