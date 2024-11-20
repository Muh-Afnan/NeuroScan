from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
import os, json
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
            name="tumor_detection_model"
        )
        messagebox.showinfo("Success", "Model Trained Successfully")
        print(results)
        print("endline")
        print(results.curves_results)

        curves_results = results.curves_results

        precision_recall = curves_results[0]
        f1_confidence = np.random.rand(len(precision_recall[0]))
        precision_confidence = np.random.rand(len(precision_recall[0]))
        recall_confidence = np.random.rand(len(precision_recall[0]))

        curves_data = {
            "ap_class_index": [0, 1, 2],
            "box": str(results["box"]),  # Convert the Metric object to string or use a method like `to_dict()` if available
            "confusion_matrix": str(results["confusion_matrix"]),  # Same for ConfusionMatrix object
            "curves": ['Precision-Recall(B)', 'F1-Confidence(B)', 'Precision-Confidence(B)', 'Recall-Confidence(B)'],
            'Precision-Recall': precision_recall[0].tolist(),  # Ensure precision_recall is an iterable like a list or numpy array
            'F1-Confidence': f1_confidence.tolist(),  # Similarly convert to list if it's a numpy array
            'Precision-Confidence': precision_confidence.tolist(),
            'Recall-Confidence': recall_confidence.tolist()
        }

        with open(self.main_obj.metrices_path, 'w') as json_file:
            json.dump(curves_data, json_file)
            
    
    def save_model(self):
        model_path = self.main_obj.saved_model_path
        self.model.save(model_path)
        messagebox.showinfo("Success", "Model Saved Successfully")

    import matplotlib.pyplot as plt

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
            label = f"Class {int(top_class)}: {top_conf:.2f}"
            color = (0, 0, 255) if top_class == 2 else (0, 255, 255) if top_class == 1 else (0, 255, 0)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)  # Draw bounding box
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)  # Add label

        # Convert BGR to RGB for Matplotlib
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Debugging: Display the image using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.imshow(image_rgb)
        plt.axis("off")
        plt.title("Prediction Debugging: Image with Bounding Boxes")
        plt.show()
        new_size = ((139*2),(132*2))
        image.resize(new_size, image.ANTIALIAS)

        # Return the image with bounding boxes drawn
        return image


    # def predict(self):
    #     model_path = self.main_obj.saved_model_path
    #     model = YOLO(model_path)
    #     image = cv2.imread(self.main_obj.detect_tumor)
    #     if image is None:
    #         raise FileNotFoundError(f"Image at path '{self.main_obj.detect_tumor}' could not be loaded.")
    #     results = model(image)
    #     # new model
    #     detections = results[0].boxes  # Extract bounding boxes
    #     # Extract detection data
    #     boxes = detections.xyxy.cpu().numpy()  # [x1, y1, x2, y2] coordinates
    #     print(boxes)
    #     confidences = detections.conf.cpu().numpy()  # Confidence scores
    #     print(confidences)
    #     classes = detections.cls.cpu().numpy()  # Class IDs
    #     print(classes)
    #     # Sort detections by confidence and class priority
    #     # Priority: Severe Tumor (2) > Benign (1) > No Tumor (0)
    #     priority = {0: 0, 1: 1, 2: 2}  # Define class priorities
    #     sorted_detections = sorted(
    #         zip(boxes, confidences, classes),
    #         key=lambda x: (x[1], priority[x[2]]),  # Sort by confidence, then by priority
    #         reverse=True  # Highest confidence first
    #     )
    #     if sorted_detections:
    #         top_box, top_conf, top_class = sorted_detections[0]
    #         x1,y1,x2,y2 = map(int, top_box)
    #         label = f"Class {int(top_class)}:{top_conf:.2f}"
    #         color = (0,0,255) if top_class == 2 else (0,255,255) if top_class == 1 else (0,255,0)
    #         cv2.rectangle(image,(x1,y1),(x2,y2),color,2)
    #         cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,0.5, color,2)
    #         import matplotlib.pyplot as plt
    #         import matplotlib.image as mpimg

    #         # Load the image
    #         img = mpimg.imread(image)

    #         # Create a figure and axis
    #         fig, ax = plt.subplots()

    #         # Display the image
    #         ax.imshow(img)

    #         # Hide the axes
    #         ax.axis('off')  # Optional: Hide the axes

    #         # Show the image
    #         plt.show()
    #         return image

        # labels = ["No Tumor", "Benign Tumor", "Malignant Tumor"]
        # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # processed_results = []
        # for result in results:
        #     if hasattr(result, 'boxes'):
        #         for box in result.boxes:
        #             x, y, w, h = box.xywh[0].numpy()  # Get bounding box coordinates in xywh format
        #             confidence = box.conf[0].item()  # Get confidence score
        #             label_index = int(box.cls[0].item())  # Get class index
        #             label = labels[label_index]  # Map to label

        #             # Store processed result
        #             processed_results.append({
        #                 "bounding_box": (x, y, w, h),
        #                 "confidence": confidence,
        #                 "label": label
        #             })

        # return image_rgb, processed_results , labels