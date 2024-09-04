from PIL import Image, ImageEnhance
import numpy as np
import os
import random

# Folder se images load karne ka function
def load_images_from_folder(folder_path):
    images = []
    # Har file ko folder me check karna
    for filename in os.listdir(folder_path):
        # Check karna agar file image hai
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)  # Image ka full path lena
            img = Image.open(img_path).convert("RGB")  # Image ko open karna aur RGB format me convert karna
            images.append((filename, img))  # Image aur filename ko list me add karna
    return images  # Images ki list return karna

# Image ko augment karne ka function
def augment_image(img, technique, *args):
    if technique == "rotate":
        angle = args[0]  # Rotation angle lena
        return img.rotate(angle)  # Image ko specified angle se ghoomana
    elif technique == "flip_horizontal":
        return img.transpose(Image.FLIP_LEFT_RIGHT)  # Image ko horizontally flip karna
    elif technique == "flip_vertical":
        return img.transpose(Image.FLIP_TOP_BOTTOM)  # Image ko vertically flip karna
    elif technique == "add_noise":
        noise_value = args[0]  # Noise ka amount lena
        np_img = np.array(img)  # Image ko numpy array me convert karna
        noise = np.random.normal(0, noise_value, np_img.shape)  # Noise create karna
        noisy_img = np_img + noise  # Image me noise add karna
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)  # Ensure karna ke pixel values 0 aur 255 ke beech me hain
        return Image.fromarray(noisy_img)  # Noisy image ko phir se PIL format me convert karna
    return img  # Agar koi valid technique specify nahi hai, to original image return karna

# YOLO model train karne ka function (placeholder)
def train_yolo_model(dataset_path, images):
    # Yahan YOLO model train karne ka code add karna
    pass
