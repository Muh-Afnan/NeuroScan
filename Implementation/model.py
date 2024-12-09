from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
from tkinter import filedialog, messagebox

class TrainModel:
    def __init__(self, main_obj):
        self.main_obj = main_obj
        # self.ui_callback = ui_callback  # Optional callback to update UI
        self.model=0
        self.y_true = None
        self.y_pred = None

    def train_model(self, epochs, batch_size, learning_rate, momentum, weight_decay, conf_threshold, nms_threshold):
        # Initialize YOLO model
        self.model = YOLO("yolov8n.pt")

        # Run YOLOv8 training with additional hyperparameters
        results = self.model.train(
            data=self.main_obj.yaml_path,
            epochs=epochs,
            imgsz=(132,139),
            batch=batch_size,
            lr0=learning_rate,
            momentum=momentum,
            weight_decay=weight_decay,
            conf=conf_threshold,
            iou=nms_threshold,
            name=self.main_obj.tumor_detection_model_path
            # name="tumor_detection_model",
            # save_dir = "c:/NeuroScan Config/"
            # project="C:/",
            # name = "run"
        )
        messagebox.showinfo("Success", "Model Trained Successfully")

    def save_model(self):
        model_path = self.main_obj.saved_model_path
        self.model.save(model_path)
        messagebox.showinfo("Success", "Model Saved Successfully")

    def predict(self):
        model_path = self.main_obj.saved_model_path
        model = YOLO(model_path)

        # Load the image using OpenCV
        image = cv2.imread(self.main_obj.detect_tumor)
        if image is None:
            raise FileNotFoundError(f"Image at path '{self.main_obj.detect_tumor}' could not be loaded.")

        # Run YOLO inference
        results = model(image)
        
        # Extract detection results
        detections = results[0].boxes  # Bounding boxes

        # Extract detection data
        boxes = detections.xyxy.cpu().numpy()  # [x1, y1, x2, y2] coordinates
        confidences = detections.conf.cpu().numpy()  # Confidence scores
        classes = detections.cls.cpu().numpy()  # Class IDs

        # Define class priorities
        priority = {0: 0, 1: 1, 2: 2}  # No Tumor (0), Benign (1), Severe Tumor (2)
        
        # Sort detections by confidence and class priority
        sorted_detections = sorted(
            zip(boxes, confidences, classes),
            key=lambda x: (x[1], priority[int(x[2])]),  # Sort by confidence, then by priority
            reverse=True
        )

        # Draw the highest-priority detection on the image
        if sorted_detections:
            top_box, top_conf, top_class = sorted_detections[0]
            x1, y1, x2, y2 = map(int, top_box)
            label = "No Tumor" if top_class == 0 else "Benign" if top_class == 1 else "Server Tumor" 
            percent_value = top_conf*100
            percent = f"{percent_value:.2f}%"
            color = (0, 0, 255) if top_class == 2 else (0, 255, 255) if top_class == 1 else (0, 255, 0)
            percent_color = (255, 255, 255)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)  # Draw bounding box
            cv2.putText(image, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)  # Add label
            cv2.putText(image, percent, (x1, y2 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, percent_color, 1)

        return image