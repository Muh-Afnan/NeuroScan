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
            batch=batch_size,
            lr0=learning_rate,
            momentum=momentum,
            weight_decay=weight_decay,
            conf=conf_threshold,
            iou=nms_threshold,
            name=self.main_obj.tumor_detection_model_path,
            patience=10
        )
        messagebox.showinfo("Success", "Model Trained Successfully")

    def save_model(self):
        model_path = self.main_obj.saved_model_path
        self.model.save(model_path)
        messagebox.showinfo("Success", "Model Saved Successfully")

    def predict(self):
        # Model ka path get karo
        model_path = self.main_obj.saved_model_path
        model = YOLO(model_path)

        # Image ko OpenCV se load karo
        image = cv2.imread(self.main_obj.detect_tumor)
        if image is None:
            raise FileNotFoundError(f"Image at path '{self.main_obj.detect_tumor}' could not be loaded.")
        
        # YOLO inference run karo
        results = model(image)
        detections = results[0].boxes  # Bounding boxes

        # Detection data ko extract karo
        boxes = detections.xyxy.cpu().numpy()  # [x1, y1, x2, y2] coordinates
        confidences = detections.conf.cpu().numpy()  # Confidence scores
        classes = detections.cls.cpu().numpy()  # Class IDs

        # Confidence threshold define karo
        confidence_threshold = 0.01

        # Confidence threshold se upar ke detections ko filter karo
        filtered_detections = [
            (box, conf, cls)
            for box, conf, cls in zip(boxes, confidences, classes)
            if conf > confidence_threshold
        ]

        # Agar koi detection nahi milti to message print karo
        if not filtered_detections:
            print("No detections above the confidence threshold.")
            return image

        # Har class ke liye highest confidence detection ko store karne ke liye dictionary initialize karo
        highest_detections = {0: None, 1: None, 2: None}

        # Har class ke liye highest confidence detection dhoondho
        for box, conf, cls in filtered_detections:
            cls = int(cls)  # Class ID ko integer mein convert karo
            if highest_detections[cls] is None or conf > highest_detections[cls][1]:
                highest_detections[cls] = (box, conf, cls)

        # Sirf highest detections ko extract karo
        final_detections = [det for det in highest_detections.values() if det is not None]

        # Detections ko visualize karo
        for box, conf, cls in final_detections:
            x1, y1, x2, y2 = map(int, box)
            # Class ke mutabiq label define karo
            label = "No Tumor" if cls == 0 else "Benign" if cls == 1 else "Malignant"
            percent_value = conf * 100
            text = f"{label} {percent_value:.1f}%"

            # Har class ke liye color define karo
            color = (0, 255, 0) if cls == 0 else (255, 0, 0) if cls == 1 else (0, 0, 255)

            # Font size aur thickness dynamically adjust karo
            font_scale = max(0.3, min(0.5, image.shape[0] / 500))
            font_thickness = max(1, int(image.shape[0] / 300))

            # Text ka size aur background calculate karo
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
            text_bg_x1, text_bg_y1 = x1, y1 - text_size[1] - 6
            text_bg_x2, text_bg_y2 = x1 + text_size[0] + 4, y1

            # Bounding box aur label ko draw karo
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
            cv2.rectangle(image, (text_bg_x1, text_bg_y1), (text_bg_x2, text_bg_y2), color, -1)
            cv2.putText(image, text, (x1 + 2, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

        return image

