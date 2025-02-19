import os
import numpy as np
import cv2
import multiprocessing
from tkinter import filedialog, messagebox
import random
import yaml


class LoadDataset:
    def __init__(self, train_frame):
        self.train_frame = train_frame
        self.mainapp_obj = train_frame.mainapp_obj
        self.select_directory()
    
    def create_yaml_file(self, yaml_filename="Brain_Tumor_Detection.yaml"):
        """Creates a YAML file with dataset paths and class names."""
        yaml_content = {
            "path": self.mainapp_obj.dataset_path,                            
            "train": os.path.join(self.mainapp_obj.training_dir, 'images'),                   
            "val": os.path.join(self.mainapp_obj.validation_dir, 'images'),                     
            "nc": 3,                                
            "names": ["No Tumor", "Benign Tumor", "Malignant Tumor"] 
        }

        with open(self.mainapp_obj.yaml_path, "w") as file:
            yaml.dump(yaml_content, file, default_flow_style=False)

    def select_directory(self):
        """Opens a dialog to select the dataset folder and initializes dataset processing."""
        dataset_folder = filedialog.askdirectory(title="Select Dataset Folder")
        self.mainapp_obj.dataset_path = dataset_folder

        if os.path.exists(self.mainapp_obj.dataset_path) and os.listdir(self.mainapp_obj.dataset_path):
            self.mainapp_obj.training_dir = os.path.join(self.mainapp_obj.dataset_path, 'Training_Dataset')
            self.mainapp_obj.validation_dir = os.path.join(self.mainapp_obj.dataset_path, 'Validation_Dataset')
            
            self.dataset_split()

    def dataset_split(self):
        """Splits dataset into training and validation sets and applies padding to images."""
        images_path = os.path.join(self.mainapp_obj.dataset_path, 'images')
        labels_path = os.path.join(self.mainapp_obj.dataset_path, 'labels')
        
        if not os.path.exists(images_path) or not os.path.exists(labels_path):
            messagebox.showerror("Error", "Images or labels folder not found!")
            return
        
        images = [img for img in os.listdir(images_path) if img.endswith(".jpg")]
        random.shuffle(images)  # Shuffle images for randomness

        # Create directories
        os.makedirs(self.mainapp_obj.training_dir, exist_ok=True)
        os.makedirs(self.mainapp_obj.validation_dir, exist_ok=True)

        # Define split sizes
        training_split = int(0.7 * len(images))
        training_images, validation_images = images[:training_split], images[training_split:]

        self.move_files(training_images, self.mainapp_obj.training_dir, images_path, labels_path)
        self.move_files(validation_images, self.mainapp_obj.validation_dir, images_path, labels_path)
        
        self.create_yaml_file()
        messagebox.showinfo("Success", "Dataset split completed successfully.")

    def move_files(self, image_list, images_path, labels_path, main_directory):
        dest_images_path = os.path.join(main_directory, 'images')
        dest_labels_path = os.path.join(main_directory, 'labels')
        os.makedirs(dest_images_path, exist_ok=True)
        os.makedirs(dest_labels_path, exist_ok=True)
        
        with multiprocessing.Pool() as pool:
            pool.starmap(self.process_image_label, [(img, images_path, labels_path, dest_images_path, dest_labels_path) for img in image_list])

    def process_image_label(self, image_filename, images_path, labels_path, dest_images_path, dest_labels_path):
        image_src = os.path.join(images_path, image_filename)
        label_filename = os.path.splitext(image_filename)[0] + ".txt"
        label_src = os.path.join(labels_path, label_filename)
        
        image = cv2.imread(image_src)
        if image is None:
            print(f"Skipping {image_filename}, unable to load.")
            return
        
        height, width = image.shape[:2]
        padding = int(0.05 * height)  # Dynamic padding (5% of height)
        new_height = height + padding
        
        # Add padding efficiently using NumPy
        padded_image = np.pad(image, ((padding, 0), (0, 0), (0, 0)), mode='constant', constant_values=0)
        padded_image = cv2.resize(padded_image, (416, 416))
        
        image_dest = os.path.join(dest_images_path, image_filename)
        cv2.imwrite(image_dest, padded_image)
        
        label_dest = os.path.join(dest_labels_path, label_filename)
        if os.path.exists(label_src):
            try:
                labels = np.loadtxt(label_src, dtype=np.float32).reshape(-1, 5)
                labels[:, 2] = (labels[:, 2] * height + padding) / new_height  # Adjust y_center
                labels[:, 4] *= height / new_height  # Adjust height
                np.savetxt(label_dest, labels, fmt="%d %.6f %.6f %.6f %.6f")
            except Exception as e:
                print(f"Error processing label for {image_filename}: {e}")
        
        print(f"Processed {image_filename} successfully")