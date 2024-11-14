import os
import numpy as np
import cv2 as cv2
from tkinter import filedialog, messagebox
import tensorflow as tf
# from tensorflow.keras import layers, Model
import random
import shutil
import yaml


class load_dataset():
    def __init__(self, train_frame):
        self.train_frame = train_frame
        self.mainapp_obj = train_frame.mainapp_obj
        self.select_directory()
    
    def create_yaml_file(self, yaml_filename="tumor_detection.yaml"):

        yaml_content = {
            "path": self.mainapp_obj.yaml_path,                           
            "train": os.path.join(self.mainapp_obj.training_dir,'images'),                   
            "val": os.path.join(self.mainapp_obj.validation_dir,'images'),                     
            "nc": 3,                                
            "names": ["No Tumor", "Mild Tumor", "Severe Tumor"] 
        }

        yaml_path = os.path.join(self.mainapp_obj.yaml_path, yaml_filename)
        with open(yaml_path, "w") as file:
            yaml.dump(yaml_content,file, default_flow_style=False)


    def select_directory(self):

        dataset_folder = filedialog.askdirectory(title="Select Dataset Folder")
        self.mainapp_obj.dataset_path = dataset_folder

        if os.path.exists(self.mainapp_obj.dataset_path) and os.listdir(self.mainapp_obj.dataset_path):
            self.mainapp_obj.training_dir = os.path.join(self.mainapp_obj.dataset_path, 'Training_Dataset')
            self.mainapp_obj.validation_dir = os.path.join(self.mainapp_obj.dataset_path, 'Validation_Dataset')
            self.mainapp_obj.testing_dir = os.path.join(self.mainapp_obj.dataset_path,'Testing_Dataset')

            self.mainapp_obj.model_path = os.path.join(self.mainapp_obj.dataset_path,"Models")
            self.mainapp_obj.yaml_path = self.mainapp_obj.model_path
            self.mainapp_obj.saved_model_path = os.path.join(self.mainapp_obj.model_path,"tumor_detection_model.pt")
            self.dataset_split()

    def dataset_split(self):
        # Define the paths for images and labels directories

        images_path = os.path.join(self.mainapp_obj.dataset_path, 'images')
        labels_path = os.path.join(self.mainapp_obj.dataset_path, 'labels')
        images = []

        # Collect all image files
        for image in os.listdir(images_path):
            if image.endswith(".jpg"):
                images.append(image)    

        # images = [f for f in os.listdir(images_path) if f.endswith(".jpg")]
        random.shuffle(images)  # Shuffle images for random splitting


        # Create directories for train/val/test splits for images and labels
        os.makedirs(self.mainapp_obj.training_dir, exist_ok=True)
        os.makedirs(self.mainapp_obj.validation_dir, exist_ok=True)
        os.makedirs(self.mainapp_obj.testing_dir, exist_ok=True)


        # Calculate dataset splits
        no_of_dataset = len(images)
        training_split = int(0.7 * no_of_dataset)
        validation_split = int(0.85 * no_of_dataset)

        # Split images into training, validation, and testing sets
        training_images = images[:training_split]
        validation_images = images[training_split:validation_split]
        testing_images = images[validation_split:]

        # Function to move image and corresponding label files
        def move_file(image_list, main_directory):
            directory_images_path = os.path.join(main_directory, 'images')
            directory_labels_path = os.path.join(main_directory, 'labels')
            os.makedirs(directory_images_path, exist_ok=True)
            os.makedirs(directory_labels_path, exist_ok=True)

            missing_count = 0

            for filename in image_list:
                # Define source paths for image and corresponding label

                image_src = os.path.join(images_path, filename)
                label_file = filename.rsplit('.', 1)[0] + ".txt"
                label_src = os.path.join(labels_path, label_file)
                
                # Define destination paths for image and label
                image_dest = os.path.join(directory_images_path, filename)
                label_dest = os.path.join(directory_labels_path, label_file)

                # Check if label file exists and move both files
                if os.path.exists(label_src):
                    shutil.move(image_src, image_dest)
                    shutil.move(label_src, label_dest)
                else:
                    missing_count +=1

        # Move files into the respective train/val/test directories
        move_file(training_images, self.mainapp_obj.training_dir)
        move_file(validation_images, self.mainapp_obj.validation_dir)
        move_file(testing_images, self.mainapp_obj.testing_dir)
    
        self.create_yaml_file(yaml_filename="tumor_detection.yaml")
        

        messagebox.showinfo("Success","Dataset split completed successfully.")