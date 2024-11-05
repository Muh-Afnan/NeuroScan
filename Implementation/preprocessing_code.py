import os
import numpy as np
import cv2 as cv2
import tensorflow as tf
from tensorflow.keras import layers, Model
import random
import shutil

class preprocessing_code():
    def __init__(self, mainapp_obj):
        self.main_obj = mainapp_obj

        self.dataset_split()
        # self.load_images_and_labels_custom()
        # self.remove_noise_custome()
        # self.create_dataset_custom()



    def dataset_split(self):
        image_extension = ('.jpg', '.png', '.jpeg', '.tiff')
        label_extension = '.txt'

        images = []

        for filename in os.listdir(self.main_obj.dataset_path):
            if filename.endswith(image_extension):
                images.append[filename]
        random.shuffle(images)

        os.makedirs(self.main_obj.training_dir , exist_ok=True)
        os.makedirs(self.main_obj.validation_dir , exist_ok=True)
        os.makedirs(self.main_obj.testing_dir , exist_ok=True)

        no_of_dataset = len(images)
        training_split = int(0.7*no_of_dataset)
        validation_split = int (0.85*no_of_dataset)

        training_images = images[:training_split]
        validation_images = images[training_split:validation_split]
        testing_images = images[validation_split:]


        def move_file(image_list, directory):
            for filename in image_list:

                label_file = filename.rsplit('.', 1) [0] + label_extension

                if os.path.exists(os.path.join(self.main_obj.directory, label_file)):
                    shutil.move(os.path.join(self.main_obj.directory,label_file),os.path.join(directory,label_file))
                    shutil.move(os.path.join(self.main_obj.directory,filename), os.path.join(directory,filename))
                else:
                    print(f"Imaged dropped {filename}")

        move_file(training_images, self.main_obj.training_dir)
        move_file(validation_images, self.main_obj.validation_dir)
        move_file(testing_images, self.main_obj.testing_dir)

    def load_images_and_labels_custom(self):
        """
        Loads images and their labels into memory.
        """

        for path in os.listdir(self.main_obj.training_dir):
            img_path=os.path.join(self.main_obj.training_dir, path)
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

    def create_dataset_custom(self):
        tf_loaded_images = tf.convert_to_tensor(self.main_obj.loaded_images)
        tf_loaded_labels = tf.ragged.constant(self.main_obj.loaded_labels, dtype=tf.float32)
        self.main_obj.dataset = tf.data.Dataset.from_tensor_slices((tf_loaded_images,tf_loaded_labels))

    def parse_yolo_label(self):
        
        labels = []
        with open(label_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center, y_center, width, height = map(float, parts[1:])
                labels.append([class_id, x_center, y_center, width, height])
        return tf.convert_to_tensor(labels)

        def load_image_with_label(image_path, label_path):
            image = tf.io.read_file(image_path)
            image = tf.image.decode_jpeg(image, channels=3)
            image = tf.image.resize(image, [256, 256])
            image /= 255.0  # Normalize to [0, 1]

            labels = parse_yolo_label(label_path)
            return image, labels


    def create_yolo_model(input_shape=(256, 256, 3), num_classes=3):
        inputs = layers.Input(shape=input_shape)

        # Convolutional layers (simple architecture for illustration)
        x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
        x = layers.MaxPooling2D(2, 2)(x)
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = layers.MaxPooling2D(2, 2)(x)
        x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = layers.MaxPooling2D(2, 2)(x)
        
        # Final layer
        outputs = layers.Conv2D(num_classes, (1, 1), activation='softmax')(x)

        model = Model(inputs, outputs)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

