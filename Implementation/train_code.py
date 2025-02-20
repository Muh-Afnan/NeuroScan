import os
import numpy as np
import cv2 as cv2
from tkinter import filedialog, messagebox
import random
import yaml

class LoadDataset():
    def __init__(self, train_frame):
        self.train_frame = train_frame  # Train frame ko initialize kar rahe hain
        self.mainapp_obj = train_frame.mainapp_obj  # Main app object ko initialize kar rahe hain
        self.select_directory()  # Dataset folder select karne ke liye function call kar rahe hain
    
    def create_yaml_file(self, yaml_filename="Brain_Tumor_Detection.yaml"):
        # Yaml file create karte hain
        yaml_content = {
            "path": self.mainapp_obj.dataset_path,  # Dataset path ka reference
            "train": os.path.join(self.mainapp_obj.training_dir,'images'),  # Training images ka path
            "val": os.path.join(self.mainapp_obj.validation_dir,'images'),  # Validation images ka path
            "nc": 3,  # Number of classes (tumor ki categories)
            "names": ["No Tumor", "Benign tumor", "Malignant tumor"]  # Classes ke names
        }

        yaml_path = self.mainapp_obj.yaml_path  # Yaml file ka path
        with open(yaml_path, "w") as file:
            yaml.dump(yaml_content,file, default_flow_style=False)  # Yaml file ko likh rahe hain


    def select_directory(self):
        # Dataset folder select karne ke liye dialog box open kar rahe hain
        dataset_folder = filedialog.askdirectory(title="Select Dataset Folder")
        self.mainapp_obj.dataset_path = dataset_folder  # Dataset ka path set kar rahe hain

        if os.path.exists(self.mainapp_obj.dataset_path) and os.listdir(self.mainapp_obj.dataset_path):
            # Agar dataset folder ka path sahi hai to training aur validation directories create karenge
            self.mainapp_obj.training_dir = os.path.normpath(os.path.join(self.mainapp_obj.dataset_path, 'Training_Dataset')).replace('\\','/')
            self.mainapp_obj.validation_dir = os.path.normpath(os.path.join(self.mainapp_obj.dataset_path, 'Validation_Dataset')).replace('\\','/')

            self.dataset_split()  # Dataset ko split karne ka function call karte hain

    def dataset_split(self):
        # Dataset ko train, validation aur test splits mein divide karte hain
        images_path = os.path.join(self.mainapp_obj.dataset_path, 'images')  # Images folder ka path
        labels_path = os.path.join(self.mainapp_obj.dataset_path, 'labels')  # Labels folder ka path
        images = []  # Image filenames ka list

        # Sare image files ko collect karte hain
        for image in os.listdir(images_path):
            if image.endswith(".jpg"):  # Sirf JPG images ko select karte hain
                images.append(image)    

        random.shuffle(images)  # Images ko randomize karte hain


        # Training aur validation ke liye directories create karte hain
        os.makedirs(self.mainapp_obj.training_dir, exist_ok=True)
        os.makedirs(self.mainapp_obj.validation_dir, exist_ok=True)

        # Total dataset ka size nikalte hain
        no_of_dataset = len(images)
        training_split = int(0.7 * no_of_dataset)  # 70% ko training ke liye allocate kar rahe hain

        # Dataset ko split karte hain
        training_images = images[:training_split]
        validation_images = images[training_split:]

        # function move_file ko call kar rahe hain images ko move karne ke liye
        move_file(training_images, self.mainapp_obj.training_dir, images_path, labels_path)
        move_file(validation_images, self.mainapp_obj.validation_dir, images_path, labels_path)
    
        self.create_yaml_file(yaml_filename="Brain_Tumor_Detection.yaml")  # Yaml file create karte hain

        messagebox.showinfo("Success", "Dataset split completed successfully.")  # Success message show karte hain

        def move_file(image_list, images_path, labels_path, main_directory):
            # Images aur labels ke liye directories create karte hain
            directory_images_path = os.path.join(main_directory, 'images')
            directory_labels_path = os.path.join(main_directory, 'labels')
            os.makedirs(directory_images_path, exist_ok=True)
            os.makedirs(directory_labels_path, exist_ok=True)

            missing_count = 0  # Missing files ka count initialize kar rahe hain

            for filename in image_list:
                # Image aur label ke source paths define karte hain
                image_src = os.path.join(images_path, filename)
                label_file = filename.rsplit('.', 1)[0] + ".txt"
                label_src = os.path.join(labels_path, label_file)

                # Destination paths ko define karte hain
                image_dest = os.path.join(directory_images_path, filename)
                label_dest = os.path.join(directory_labels_path, label_file)

                if os.path.exists(label_src):  # Agar label file exist karti hai
                    try:
                        image = cv2.imread(image_src)  # Image ko load karte hain
                        if image is None:  # Agar image load nahi hoti
                            print(f"Failed to load image: {image_src}")
                            missing_count += 1
                            continue

                        height, width = image.shape[:2]  # Image ke height aur width ko extract karte hain

                        if height != width:  # Agar image square nahi hai
                            # Padding add karte hain taake image square ho jaye
                            new_size = max(height, width)

                            # Padding calculate karte hain
                            top_padding = (new_size - height) // 2
                            bottom_padding = new_size - height - top_padding
                            left_padding = (new_size - width) // 2
                            right_padding = new_size - width - left_padding

                            # Image ko padding ke saath save karte hain
                            padded_image = cv2.copyMakeBorder(image, top_padding, bottom_padding, left_padding, right_padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
                            cv2.imwrite(image_dest, padded_image)

                            # Label coordinates ko adjust karte hain using NumPy vectorization
                            labels = np.loadtxt(label_src)  # Label data ko NumPy array mein load karte hain
                            # Vectorized adjustment
                            x_center = (labels[:, 1] * width + left_padding) / new_size
                            y_center = (labels[:, 2] * height + top_padding) / new_size
                            width_new = labels[:, 3] * width / new_size
                            height_new = labels[:, 4] * height / new_size

                            # Adjusted labels ko save karte hain
                            adjusted_labels = np.column_stack((labels[:, 0], x_center, y_center, width_new, height_new))  # Class_id aur new coordinates ko combine karte hain
                            np.savetxt(label_dest, adjusted_labels, fmt='%d %.16f %.16f %.16f %.16f')  # Adjusted labels ko save karte hain

                            print(f"Image and label {filename} padded successfully.")
                        else:
                            # Square images ko directly move karte hain bina padding ke
                            cv2.imwrite(image_dest, image)
                            os.replace(label_src, label_dest)
                            print(f"Image and label {filename} moved without padding.")
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
                        missing_count += 1
                else:
                    missing_count += 1

            print(f"Process completed with {missing_count} missing files.")  # Missing files ki count print karte hain
