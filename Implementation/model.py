from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_curve, f1_score
import cv2 as cv2
from tkinter import filedialog

class TrainModel:
    def __init__(self, main_obj):
        self.main_obj = main_obj
        # self.ui_callback = ui_callback  # Optional callback to update UI
        self.model=0

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
            name="tumor_detection_model"
        )
        print("Training complete.")

    def generate_confusion_matrix(self):
        # Assuming `self.model.val()` returns the validation results with true labels and predictions
        val_results = self.model.val()  
        y_true = val_results["labels"]
        y_pred = val_results["preds"]

        # Generate confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title("Confusion Matrix")
        plt.colorbar()
        tick_marks = np.arange(len(self.main_obj.class_labels))
        plt.xticks(tick_marks, self.main_obj.class_labels, rotation=45)
        plt.yticks(tick_marks, self.main_obj.class_labels)
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()

    def generate_f1_curve(self):
        # Assuming `self.model.metrics()` provides F1 scores over epochs
        f1_scores = self.model.metrics()["f1"]
        epochs = range(1, len(f1_scores) + 1)

        plt.figure(figsize=(8, 6))
        plt.plot(epochs, f1_scores, label="F1 Score", color="blue")
        plt.xlabel("Epochs")
        plt.ylabel("F1 Score")
        plt.title("F1 Score Curve")
        plt.legend()
        plt.show()

    def generate_pr_curve(self):
        val_results = self.model.val()
        y_true = val_results["labels"]
        y_scores = val_results["scores"]

        precision, recall, _ = precision_recall_curve(y_true, y_scores)

        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, label="PR Curve", color="green")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("Precision-Recall Curve")
        plt.legend()
        plt.show()

    def generate_precision_curve(self):
        # Assuming `self.model.metrics()` provides precision scores at different confidence thresholds
        precisions = self.model.metrics()["precision"]
        confidence = self.model.metrics()["confidence"]

        plt.figure(figsize=(8, 6))
        plt.plot(confidence, precisions, label="Precision", color="orange")
        plt.xlabel("Confidence Threshold")
        plt.ylabel("Precision")
        plt.title("Precision Curve")
        plt.legend()
        plt.show()

    def generate_recall_curve(self):
        # Assuming `self.model.val()` returns the validation results as a DetMetrics object
        val_results = self.model.val()

        # Accessing the labels and predictions from the DetMetrics object
        y_true = val_results.labels  # This assumes the `labels` attribute exists in DetMetrics
        y_pred = val_results.pred  # This assumes the `pred` attribute exists in DetMetrics

        # Generate confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title("Confusion Matrix")
        plt.colorbar()
        tick_marks = np.arange(len(self.main_obj.class_labels))
        plt.xticks(tick_marks, self.main_obj.class_labels, rotation=45)
        plt.yticks(tick_marks, self.main_obj.class_labels)
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()


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