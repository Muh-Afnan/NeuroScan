from ultralytics import YOLO
import cv2 as cv2
from tkinter import filedialog

class TrainModel:
    def __init__(self, main_obj):
        self.main_obj = main_obj
        # self.ui_callback = ui_callback  # Optional callback to update UI
        self.model=0

    def train_model(self, epochs,batch_size, learning_rate, momentum,weight_decay,conf_threshold, nms_threshold ):
        # Initialize YOLO model
        self.model = YOLO("yolov8n.pt")

        # Run YOLOv8 training with additional hyperparameters
        results = self.model.train(
            # data=self.main_obj.yaml_path,  # Path to YAML file
            data = "D:/Project/NeuroScan/dataset/Models/Brain_Tumor_Detection.yaml",
            epochs=epochs,                 # Number of training epochs
            imgsz=(132,139),                     # Image size
            batch=batch_size,              # Batch size
            lr0=learning_rate,             # Learning rate
            momentum=momentum,             # Momentum
            weight_decay=weight_decay,     # Weight decay (L2 regularization)
            conf=conf_threshold,           # Confidence threshold
            iou=nms_threshold,             # NMS threshold
            name="tumor_detection_model"
        )
        print("Training complete.")

    def save_model(self):
        model_path = self.main_obj.saved_model_path
        self.model.save(model_path)

    def predict(self):
        model_path = self.main_obj.saved_model_path
        model = YOLO(model_path)
        image = cv2.imread(self.main_obj.detect_tumor)
        results = model(image)
        labels = ["No Tumor", "Mild Tumor", "Severe Tumor"]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image_rgb, results, labels
