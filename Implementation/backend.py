from PIL import Image, ImageEnhance
import numpy as np
import os
import random

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path).convert("RGB")
            images.append((filename, img))
    return images


def augment_image(img, technique, *args):
    if technique == "rotate":
        angle = args[0]
        return img.rotate(angle)
    elif technique == "flip_horizontal":
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif technique == "flip_vertical":
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    elif technique == "add_noise":
        noise_value = args[0]
        np_img = np.array(img)
        noise = np.random.normal(0, noise_value, np_img.shape)
        noisy_img = np_img + noise
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_img)
    # Add more augmentation techniques as needed
    return img

def train_yolo_model(dataset_path, images):
    # Implement YOLO training here
    pass
