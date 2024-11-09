import os
import numpy as np
import cv2 as cv2
import tensorflow as tf
# from tensorflow.keras import layers, Model
import random
import shutil

class load_dataset():
    def __init__(self, train_frame):
        self.train_frame = train_frame
        self.mainapp_obj = train_frame.mainapp_obj
        self.dataset_split()

    def dataset_split(self):
        # Define the paths for images and labels directories
        # self.mainapp_obj.dataset_path = os.path.abspath(self.mainapp_obj)  # Make sure it's an absolute path
        images_path = os.path.join(self.mainapp_obj, 'images')
        labels_path = os.path.join(self.mainapp_obj, 'labels')
        images = []
        # Collect all image files
        for image in os.listdir(images_path):
            if image.endswith(".jpg"):
                images.append(image)    

        # images = [f for f in os.listdir(images_path) if f.endswith(".jpg")]
        random.shuffle(images)  # Shuffle images for random splitting

        # Create directories for train/val/test splits for images and labels
        os.makedirs(self.train_frame.training_dir_images, exist_ok=True)
        os.makedirs(self.train_frame.validation_dir_images, exist_ok=True)
        os.makedirs(self.train_frame.testing_dir_images, exist_ok=True)

        os.makedirs(self.train_frame.training_dir_label, exist_ok=True)
        os.makedirs(self.train_frame.validation_dir_label, exist_ok=True)
        os.makedirs(self.train_frame.testing_dir_label, exist_ok=True)

        # Calculate dataset splits
        no_of_dataset = len(images)
        training_split = int(0.7 * no_of_dataset)
        validation_split = int(0.85 * no_of_dataset)

        # Split images into training, validation, and testing sets
        training_images = images[:training_split]
        validation_images = images[training_split:validation_split]
        testing_images = images[validation_split:]

        # Function to move image and corresponding label files
        def move_file(image_list, image_directory, label_directory):
            for filename in image_list:
                # Define source paths for image and corresponding label
                image_src = os.path.join(images_path, filename)
                label_file = filename.rsplit('.', 1)[0] + ".txt"
                label_src = os.path.join(labels_path, label_file)
                
                # Define destination paths for image and label
                image_dest = os.path.join(image_directory, filename)
                label_dest = os.path.join(label_directory, label_file)

                # Check if label file exists and move both files
                if os.path.exists(label_src):
                    shutil.move(image_src, image_dest)
                    shutil.move(label_src, label_dest)
                else:
                    print(f"Label file missing for image: {filename}. Image dropped.")

        # Move files into the respective train/val/test directories
        move_file(training_images, self.train_frame.training_dir_images, self.train_frame.training_dir_label)
        move_file(validation_images, self.train_frame.validation_dir_images, self.train_frame.validation_dir_label)
        move_file(testing_images, self.train_frame.testing_dir_images, self.train_frame.testing_dir_label)

        print("Dataset split completed successfully.")