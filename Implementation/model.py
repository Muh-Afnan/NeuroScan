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
            data = self.main_obj.yaml_path,
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

    def generate_confusion_matrix(self):
        return self.model.get_confusion_matrix()
    
    def generate_f1_scroe(self):
        return self.model.get_f1_curve()

    def save_model(self):
        model_path = self.main_obj.saved_model_path
        self.model.save(model_path)

    def predict(self):
        model_path = self.main_obj.saved_model_path
        model = YOLO(model_path)
        image = cv2.imread(self.main_obj.detect_tumor)
        if image is None:
            raise FileNotFoundError(f"Image at path '{self.main_obj.detect_tumor}' could not be loaded.")
        results = model(image)
        labels = ["No Tumor", "Benign Tumor", "Malignant Tumor"]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        processed_results = []
        for result in results:
            if hasattr(result, 'boxes'):
                for box in result.boxes:
                    x, y, w, h = box.xywh[0].numpy()  # Get bounding box coordinates in xywh format
                    confidence = box.conf[0].item()  # Get confidence score
                    label_index = int(box.cls[0].item())  # Get class index
                    label = labels[label_index]  # Map to label

                    # Store processed result
                    processed_results.append({
                        "bounding_box": (x, y, w, h),
                        "confidence": confidence,
                        "label": label
                    })

        return image_rgb, processed_results , labels