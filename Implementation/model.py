from ultralytics import YOLO
import numpy as np
import cv2 as cv2
from tkinter import messagebox

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
        )
        messagebox.showinfo("Success", "Model Trained Successfully")

    def save_model(self):
        model_path = self.main_obj.saved_model_path
        self.model.save(model_path)
        messagebox.showinfo("Success", "Model Saved Successfully")

    # def predict(self):
    #     model_path = self.main_obj.saved_model_path
    #     model = YOLO(model_path)

    #     # Load the image using OpenCV
    #     image = cv2.imread(self.main_obj.detect_tumor)
    #     if image is None:
    #         raise FileNotFoundError(f"Image at path '{self.main_obj.detect_tumor}' could not be loaded.")

    #     # Run YOLO inference
    #     results = model(image)
        
    #     # Extract detection results
    #     detections = results[0].boxes  # Bounding boxes

    #     # Extract detection data
    #     boxes = detections.xyxy.cpu().numpy()  # [x1, y1, x2, y2] coordinates
    #     confidences = detections.conf.cpu().numpy()  # Confidence scores
    #     classes = detections.cls.cpu().numpy()  # Class IDs



    #     priority = {2:0,1:1,0:2}
    #     confidence_threshold = 0.1
    #     filtered_detections = [
    #         (box, conf, cls) for box, conf, cls in zip(boxes, confidences, classes)
    #     ]
    #     print(filtered_detections)

    #     sorted_detections = sorted(
    #     filtered_detections,
    #     key=lambda x: (x[1], -priority[int(x[2])]),  # Sort by confidence, then by priority
    #     reverse=True
    #     )   

    #     # Old Code
    #     # # Define class priorities
    #     # priority = {0: 0, 1: 1, 2: 2}  # No Tumor (0), Benign (1), Severe Tumor (2)
        
    #     # # Sort detections by confidence and class priority
    #     # sorted_detections = sorted(
    #     #     zip(boxes, confidences, classes),
    #     #     key=lambda x: (x[1], priority[int(x[2])]),  # Sort by confidence, then by priority
    #     #     reverse=True
    #     # )
    #     if sorted_detections:
    #         top_box, top_conf, top_class = sorted_detections[0]
    #         x1, y1, x2, y2 = map(int, top_box)
    #         label = "No Tumor" if top_class == 0 else "Benign" if top_class == 1 else "Severe Tumor"
    #         percent_value = top_conf * 100
    #         text = f"{label} {percent_value:.2f}%"
            
    #         # Define colors for each class
    #         color = (0, 0, 255) if top_class == 2 else (255, 0, 0) if top_class == 1 else (0, 255, 0)
            
    #         # Dynamically adjust font size and thickness based on image dimensions
    #         font_scale = 0.3
    #         font_thickness = 1
            
    #         # Get text size
    #         text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
            
    #         # Calculate text background rectangle
    #         text_x, text_y = x1, y1 - 5
    #         text_bg_x1, text_bg_y1 = x1, y1 - text_size[1] - 6  # Text background top-left
    #         text_bg_x2, text_bg_y2 = x1 + text_size[0] + 4, y1  # Text background bottom-right

    #         # Draw the bounding box
    #         cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)  # Bounding box with thicker lines

    #         # Draw text background rectangle
    #         cv2.rectangle(image, (text_bg_x1, text_bg_y1), (text_bg_x2, text_bg_y2), color, -1)  # Filled rectangle

    #         # Draw text on top of the filled rectangle
    #         cv2.putText(image, text, (text_x + 2, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

    #     return image


    # single Predection.
    def predict(self):
        model_path = self.main_obj.saved_model_path
        model = YOLO(model_path)

        # Load the image using OpenCV
        image = cv2.imread(self.main_obj.detect_tumor)
        if image is None:
            raise FileNotFoundError(f"Image at path '{self.main_obj.detect_tumor}' could not be loaded.")

        # Run YOLO inference
        results = model(image)
        detections = results[0].boxes  # Bounding boxes

        # Extract detection data
        boxes = detections.xyxy.cpu().numpy()  # [x1, y1, x2, y2] coordinates
        confidences = detections.conf.cpu().numpy()  # Confidence scores
        classes = detections.cls.cpu().numpy()  # Class IDs

        # Define class priorities
        priority = {2: 0, 1: 1, 0: 2}  # Severe Tumor (2), Benign (1), No Tumor (0)
        confidence_threshold = 0.1

        # Filter and sort detections
        filtered_detections = [
            (box, conf, cls)
            for box, conf, cls in zip(boxes, confidences, classes)
            if conf > confidence_threshold
        ]

        sorted_detections = sorted(
            filtered_detections,
            key=lambda x: (x[1], -priority[int(x[2])]),  # Sort by confidence, then by priority
            reverse=True
        )

        if not sorted_detections:
            print("No detections above the confidence threshold.")
            return image

        # Select the top detection
        top_box, top_conf, top_class = sorted_detections[0]
        x1, y1, x2, y2 = map(int, top_box)
        label = "No Tumor" if top_class == 0 else "Benign" if top_class == 1 else "Severe Tumor"
        percent_value = top_conf * 100
        text = f"{label} {percent_value:.1f}%"

        # Define colors for each class
        color = (0, 0, 255) if top_class == 2 else (255, 0, 0) if top_class == 1 else (0, 255, 0)

        # Dynamically adjust font size and thickness
        font_scale = max(0.3, min(0.5, image.shape[0] / 500))
        font_thickness = max(1, int(image.shape[0] / 300))

        # Calculate text size and background
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
        text_bg_x1, text_bg_y1 = x1, y1 - text_size[1] - 6
        text_bg_x2, text_bg_y2 = x1 + text_size[0] + 4, y1

        # Draw bounding box and label
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
        cv2.rectangle(image, (text_bg_x1, text_bg_y1), (text_bg_x2, text_bg_y2), color, -1)
        cv2.putText(image, text, (x1 + 2, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)


        # if not filtered_detections:
        #     print("No detections above the confidence threshold.")
        #     return image

        # # Loop through each detection and display it
        # for box, conf, cls in filtered_detections:
        #     x1, y1, x2, y2 = map(int, box)
        #     label = "No Tumor" if cls == 0 else "Benign" if cls == 1 else "Severe Tumor"
        #     percent_value = conf * 100
        #     text = f"{label} {percent_value:.1f}%"

        #     # Define colors for each class
        #     color = (0, 0, 255) if cls == 2 else (255, 0, 0) if cls == 1 else (0, 255, 0)

        #     # Dynamically adjust font size and thickness
        #     font_scale = max(0.3, min(0.5, image.shape[0] / 500))
        #     font_thickness = max(1, int(image.shape[0] / 300))

        #     # Calculate text size and background
        #     text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
        #     text_bg_x1, text_bg_y1 = x1, y1 - text_size[1] - 6
        #     text_bg_x2, text_bg_y2 = x1 + text_size[0] + 4, y1

        #     # Draw bounding box and label
        #     cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
        #     cv2.rectangle(image, (text_bg_x1, text_bg_y1), (text_bg_x2, text_bg_y2), color, -1)
        #     cv2.putText(image, text, (x1 + 2, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

        return image
