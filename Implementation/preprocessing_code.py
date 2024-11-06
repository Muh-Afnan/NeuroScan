import os
import numpy as np
import cv2 as cv2
import tensorflow as tf
from ultralytics import YOLO
from tensorflow.keras import layers, Model
import random
import shutil
from ultralytics import YOLO

class preprocessing_code():
    def __init__(self, mainapp_obj):
        self.main_obj = mainapp_obj
        self.dataset_split()
        # self.load_images_and_labels_custom()
        # self.remove_noise_custome()
        # self.create_dataset_custom()

    
    def load_images_and_labels_custom(self):
        """
        Loads images and their labels into memory.
        """

        for path in os.listdir(self.main_obj.dataset_path):
            img_path=os.path.join(self.main_obj.dataset_path, path)
            image = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Image at path {img_path} could not be loaded")
                continue
            self.main_obj.loaded_images.append(image)

            # Load the Label
            individual_label = []

            label_file = path.rsplit('.', 1)[0] + ".txt"
            lbl_path = os.path.join(self.main_obj.training_dir, label_file)

            with open(lbl_path, 'r') as file:
                labels = file.readlines()

            for label in labels:
                parts = label.strip().split()
                class_id = int(parts[0])
                x_center = float(parts[1]) * 139
                y_center = float(parts[2]) * 132
                box_width = float(parts[3]) * 139
                box_height = float(parts[4]) * 132

                x_min = int(x_center - box_width/2)
                y_min = int(y_center - box_height/2)
                x_max = int(x_center + box_width/2)
                y_max = int(y_center + box_height/2)

                individual_label.append([class_id, x_min, y_min, x_max, y_max])
        
            self.main_obj.loaded_label.append(individual_label)
            
    def remove_noise_custome(self,filter_strength=10, template_window_size=7, search_window_size=21):
            """
            Removes noise from images using fastNlMeansDenoising.
            """
            for i in range(len(self.main_obj.loaded_images)):
                if len(self.main_obj.loaded_images[i].shape) == 3:
                    self.main_obj.loaded_images[i] = cv2.fastNlMeansDenoisingColored(
                        self.main_obj.loaded_images[i], None, filter_strength, filter_strength,
                        template_window_size, search_window_size
                    )
                else:
                    self.main_obj.loaded_images[i] = cv2.fastNlMeansDenoising(
                        self.main_obj.loaded_images[i], None, filter_strength, 
                        template_window_size, search_window_size
                    )

    def preprocess_and_save(self):
        """
        Load images, apply preprocessing (e.g., noise removal), and save the processed images.
        """
        for image_filename in os.listdir(self.main_obj.dataset_path):
            # Load image
            image_path = os.path.join(self.main_obj.dataset_path, image_filename)
            image = cv2.imread(image_path)

            # Apply preprocessing (e.g., noise removal)
            if image is not None:
                image = self.remove_noise_custome(image)  # Your custom preprocessing function
                # Save preprocessed image back in the same directory
                processed_image_path = os.path.join(self.main_obj.training_dir_images, image_filename)
                cv2.imwrite(processed_image_path, image)
            else:
                print(f"Image {image_filename} could not be loaded and was skipped.")

        # Optional: Process labels if needed (e.g., if coordinates need adjustment)
        for label_filename in os.listdir(self.main_obj.dataset_path):
            label_path = os.path.join(self.main_obj.dataset_path, label_filename)
            # No processing needed for labels in this case, but can be added if required.
            shutil.copy(label_path, os.path.join(self.main_obj.dataset_path, label_filename))

    def dataset_split(self):
        # Define the paths for images and labels directories
        images_path = os.path.join(self.main_obj.dataset_path, 'images')
        labels_path = os.path.join(self.main_obj.dataset_path, 'labels')
        images = []
        # Collect all image files
        for image in os.listdir(images_path):
            if image.endswith(".jpg"):
                images.append(image)    

        # images = [f for f in os.listdir(images_path) if f.endswith(".jpg")]
        random.shuffle(images)  # Shuffle images for random splitting

        # Create directories for train/val/test splits for images and labels
        os.makedirs(self.main_obj.training_dir_images, exist_ok=True)
        os.makedirs(self.main_obj.validation_dir_images, exist_ok=True)
        os.makedirs(self.main_obj.testing_dir_images, exist_ok=True)

        os.makedirs(self.main_obj.training_dir_label, exist_ok=True)
        os.makedirs(self.main_obj.validation_dir_label, exist_ok=True)
        os.makedirs(self.main_obj.testing_dir_label, exist_ok=True)

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
        move_file(training_images, self.main_obj.training_dir_images, self.main_obj.training_dir_label)
        move_file(validation_images, self.main_obj.validation_dir_images, self.main_obj.validation_dir_label)
        move_file(testing_images, self.main_obj.testing_dir_images, self.main_obj.testing_dir_label)

        print("Dataset split completed successfully.")

        def create_yaml_config():
            yaml_content = f"""
            path: {self.main_obj.dataset_path}
            train: {self.main_obj.training_dir_images}
            val: {self.main_obj.validation_dir_images}
            test: {self.main_obj.testing_dir_images}

            nc: 3
            names: ["No Tumor", "Middle Tumor", "Severe Tumor"]
            """

            yaml_path = os.path.join(self.main_obj.dataset_path, "tumor_detection.yaml")
            with open(yaml_path, 'w') as yaml_file:
                yaml_file.write(yaml_content.strip())
            print(f"YAML configuration file created at {yaml_path}")
            return yaml_path

        # Generate the YAML file and save the path
        self.main_obj.yaml_path = create_yaml_config()    


    def train_model(self):
        model = YOLO("yolov8n.pt")  # 'yolov8n.pt' is for Nano, 'yolov8s.pt' is for Small, etc.

        # Train the model
        results = model.train(
            data=self.main_obj.yaml_path,  # Path to YAML configuration file
            epochs=50,                              # Number of training epochs
            imgsz=640,                              # Image size
            batch=16,                               # Batch size
            name="tumor_detection_model"             # Model name for saving
        )

        print("Training complete.")