
        # Function to move image and corresponding label files
        # def move_file(image_list, main_directory):
        #     directory_images_path = os.path.join(main_directory, 'images')
        #     directory_labels_path = os.path.join(main_directory, 'labels')
        #     os.makedirs(directory_images_path, exist_ok=True)
        #     os.makedirs(directory_labels_path, exist_ok=True)

        #     missing_count = 0

        #     for filename in image_list:
        #         # Define source paths for image and corresponding label

        #         image_src = os.path.join(images_path, filename)
        #         label_file = filename.rsplit('.', 1)[0] + ".txt"
        #         label_src = os.path.join(labels_path, label_file)
                
        #         # Define destination paths for image and label
        #         image_dest = os.path.join(directory_images_path, filename)
        #         label_dest = os.path.join(directory_labels_path, label_file)

        #         # Check if label file exists and move both files
        #         if os.path.exists(label_src):
        #             # adding padding to image
        #             image = cv2.imread(image_src)
        #             padding = 7
        #             padded_image = cv2.copyMakeBorder(image, padding, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        #             padded_image = cv2.resize(416,416)
        #             cv2.imwrite(image_dest, padded_image)

        #             # adjusting label accordingly
        #             original_height = 132
        #             new_height = original_height + padding

        #             with open(label_src, "r") as infile, open(label_src, "w") as outfile:
        #                 for line in infile:
        #                     class_id, x_center, y_center, width, height = map(float, line.split())
                            
        #                     # Adjust y_center and height for the new image height
        #                     y_center_new = (y_center * original_height + padding / 2) / new_height
        #                     height_new = height * original_height / new_height
                            
        #                     # Write adjusted labels
        #                     outfile.write(f"{int(class_id)} {x_center:.6f} {y_center_new:.6f} {width:.6f} {height_new:.6f}\n")

        #             # shutil.move(image_src, image_dest)
        #             shutil.move(label_src, label_dest)
        #         else:
        #             missing_count +=1


# Old Traing File
import os
import numpy as np
import cv2 as cv2
from tkinter import filedialog, messagebox
import random
import shutil
import yaml


class load_dataset():
    def __init__(self, train_frame):
        self.train_frame = train_frame
        self.mainapp_obj = train_frame.mainapp_obj
        self.select_directory()
    
    def create_yaml_file(self, yaml_filename="Brain_Tumor_Detection.yaml"):
        yaml_content = {
            "path": self.mainapp_obj.dataset_path,                           
            "train": os.path.join(self.mainapp_obj.training_dir,'images'),                   
            "val": os.path.join(self.mainapp_obj.validation_dir,'images'),                     
            "nc": 3,                                
            "names": ["No Tumor", "Benign tumor", "Malignant tumor"] 
        }

        yaml_path = self.mainapp_obj.yaml_path
        with open(yaml_path, "w") as file:
            yaml.dump(yaml_content,file, default_flow_style=False)


    def select_directory(self):

        dataset_folder = filedialog.askdirectory(title="Select Dataset Folder")
        self.mainapp_obj.dataset_path = dataset_folder

        if os.path.exists(self.mainapp_obj.dataset_path) and os.listdir(self.mainapp_obj.dataset_path):
            self.mainapp_obj.training_dir = os.path.normpath(os.path.join(self.mainapp_obj.dataset_path, 'Training_Dataset')).replace('\\','/')
            self.mainapp_obj.validation_dir = os.path.normpath(os.path.join(self.mainapp_obj.dataset_path, 'Validation_Dataset')).replace('\\','/')

            
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

        random.shuffle(images)  # Shuffle images for random splitting


        # Create directories for train/val/test splits for images and labels
        os.makedirs(self.mainapp_obj.training_dir, exist_ok=True)
        os.makedirs(self.mainapp_obj.validation_dir, exist_ok=True)
        # os.makedirs(self.mainapp_obj.model_path, exist_ok=True)


        # Calculate dataset splits
        no_of_dataset = len(images)
        training_split = int(0.7 * no_of_dataset)

        # Split images into training, validation, and testing sets
        training_images = images[:training_split]
        validation_images = images[training_split:]

        def move_file(image_list, main_directory):
            # Create directories for images and labels
            directory_images_path = os.path.join(main_directory, 'images')
            directory_labels_path = os.path.join(main_directory, 'labels')
            os.makedirs(directory_images_path, exist_ok=True)
            os.makedirs(directory_labels_path, exist_ok=True)

            missing_count = 0
            padding = 7
            original_height = 132
            new_height = original_height + padding

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
                    try:
                        # Add padding to image
                        image = cv2.imread(image_src)
                        if image is None:
                            print(f"Failed to load image: {image_src}")
                            missing_count += 1
                            continue

                        padded_image = cv2.copyMakeBorder(image, padding, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                        padded_image = cv2.resize(padded_image, (416, 416))
                        cv2.imwrite(image_dest, padded_image)
                        print(f"Image {padded_image} is padded sucessfully")

                        # Adjust label coordinates
                        temp_label_dest = label_dest + ".temp"
                        with open(label_src, "r") as infile, open(temp_label_dest, "w") as outfile:
                            for line in infile:
                                class_id, x_center, y_center, width, height = map(float, line.split())
                                
                                # Adjust y_center and height for the new image height
                                y_center_new = (y_center * original_height + padding) / new_height
                                height_new = height * original_height / new_height
                                
                                # Write adjusted labels
                                outfile.write(f"{int(class_id)} {x_center:.6f} {y_center_new:.6f} {width:.6f} {height_new:.6f}\n")
                        
                        # Replace the original label with the updated one
                        os.replace(temp_label_dest, label_dest)
                        print(f"Label {padded_image} is padded sucessfully")
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
                        missing_count += 1
                else:
                    missing_count += 1

        # Move files into the respective train/val/test directories
        move_file(training_images, self.mainapp_obj.training_dir)
        move_file(validation_images, self.mainapp_obj.validation_dir)
    
        self.create_yaml_file(yaml_filename="Brain_Tumor_Detection.yaml")
            

        messagebox.showinfo("Success","Dataset split completed successfully.")



import os
import numpy as np
import cv2
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
            "path": self.mainapp_obj.dataset_path,  # Dataset root path
            "train": os.path.join(self.mainapp_obj.training_dir, 'images'),  # Training images path
            "val": os.path.join(self.mainapp_obj.validation_dir, 'images'),  # Validation images path
            "nc": 3,  # Number of classes (No Tumor, Benign Tumor, Malignant Tumor)
            "names": ["No Tumor", "Benign Tumor", "Malignant Tumor"]  # Class names
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

        self.move_files(training_images, images_path, labels_path, self.mainapp_obj.training_dir)
        self.move_files(validation_images, images_path, labels_path, self.mainapp_obj.validation_dir)
        
        self.create_yaml_file()
        messagebox.showinfo("Success", "Dataset split completed successfully.")

    def move_files(self, image_list, images_path, labels_path, main_directory):
        dest_images_path = os.path.join(main_directory, 'images')
        dest_labels_path = os.path.join(main_directory, 'labels')
        os.makedirs(dest_images_path, exist_ok=True)
        os.makedirs(dest_labels_path, exist_ok=True)

        for img in image_list:
            self.process_image_label(img, images_path, labels_path, dest_images_path, dest_labels_path)

    def process_image_label(self, image_filename, images_path, labels_path, dest_images_path, dest_labels_path):
        image_src = os.path.join(images_path, image_filename)
        label_filename = os.path.splitext(image_filename)[0] + ".txt"
        label_src = os.path.join(labels_path, label_filename)
        
        image = cv2.imread(image_src)
        if image is None:
            print(f"Skipping {image_filename}, unable to load.")
            return
        
        height, width = image.shape[:2]
        new_size = max(height, width)
        
        # Add padding efficiently using NumPy
        if height != width:
            top_padding = (new_size - height) // 2
            bottom_padding = new_size - height - top_padding
            left_padding = (new_size - width) // 2
            right_padding = new_size - width - left_padding

            padded_image = cv2.copyMakeBorder(image, top_padding, bottom_padding, left_padding, right_padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            image_dest = os.path.join(dest_images_path, image_filename)
            cv2.imwrite(image_dest, padded_image)
        else:
            image_dest = os.path.join(dest_images_path, image_filename)
            cv2.imwrite(image_dest, image)

        # Check if label file exists and has data
        if os.path.exists(label_src):
            try:
                with open(label_src, 'r') as file:
                    lines = file.readlines()
                    if not lines:
                        print(f"Skipping {image_filename}, label file is empty.")
                        return

                labels = np.loadtxt(label_src, dtype=np.float32).reshape(-1, 5)
                if height != width:
                    # Vectorized label adjustment
                    labels[:, 1] = (labels[:, 1] * width + left_padding) / new_size  # Adjust x_center
                    labels[:, 2] = (labels[:, 2] * height + top_padding) / new_size  # Adjust y_center
                    labels[:, 3] *= width / new_size  # Adjust width
                    labels[:, 4] *= height / new_size  # Adjust height
                np.savetxt(os.path.join(dest_labels_path, label_filename), labels, fmt="%d %.6f %.6f %.6f %.6f")
            except Exception as e:
                print(f"Error processing label for {image_filename}: {e}")
                print(f"Label content: {lines if 'lines' in locals() else 'N/A'}")
        else:
            print(f"Skipping {image_filename}, label file is missing.")
