import os
import numpy as np
import cv2 as cv2
import tensorflow
import random
import shutil

class preprocessing_code():
    def __init__(self, mainapp_obj):
        self.main_obj = mainapp_obj

        self.dataset_split()



    def dataset_split(self):
        image_extension = ('.jpg', '.png', '.jpeg', '.tiff')
        label_extension = '.txt'

        images = []

        for filename in os.listdir(self.main_obj.dataset_path):
            if filename.endswith(image_extension):
                images.append[filename]
        random.shuffle(images)

        os.makedirs(self.mainobj.training_dir , exist_ok=True)
        os.makedirs(self.mainobj.validation_dir , exist_ok=True)
        os.makedirs(self.mainobj.testing_dir , exist_ok=True)

        no_of_dataset = len(images)
        training_split = int(0.7*no_of_dataset)
        validation_split = int (0.85*no_of_dataset)

        training_images = images[:training_split]
        validation_images = images[training_split:validation_split]
        testing_images = images[validation_split:]


        def move_file(image_list, directory):
            for filename in image_list:

                label_file = filename.rsplit('.', 1) [0] + label_extension

                if os.path.exists(os.path.join(self.mainobj.directory, label_file)):
                    shutil.move(os.path.join(self.mainobj.directory,label_file),os.path.join(directory,label_file))
                    shutil.move(os.path.join(self.mainobj.directory,filename), os.path.join(directory,filename))
                else:
                    print(f"Imaged dropped {filename}")

        move_file(training_images, self.mainobj.training_dir)
        move_file(validation_images, self.mainobj.validation_dir)
        move_file(testing_images, self.mainobjtesting_dir)

    def load_images_and_labels(self):
        """
        Loads images and their labels into memory.
        """

        for path in os.listdir(self.main_obj.training_dir):
            if os.
            dataset_path=os.path.join(self.main_obj.training_dir,path )

        for img_path, lbl_path in zip(self.main_obj.image_paths, self.main_obj.label_paths):
            # Load the image
            image = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Image at path {img_path} could not be loaded")
            self.main_obj.loaded_images.append(image)
            self.main_obj.loaded_labels.append()
            # Load the Label
            individual_label = []

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


def parse_label(label_path, image_width, image_height):
    bounding_boxes = []

    with open(label_path, 'r') as file:
        labels = file.readlines()

    for label in labels:
        parts = label.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1]) * image_width
        y_center = float(parts[2]) * image_height
        box_width = float(parts[3]) * image_width
        box_height = float(parts[4]) * image_height

        x_min = int(x_center - box_width/2)
        y_min = int(y_center - box_height/2)
        x_max = int(x_center + box_width/2)
        y_max = int(y_center + box_height/2)

        bounding_boxes.append([class_id, x_min, y_min, x_max, y_max])

    return bounding_boxes
            

