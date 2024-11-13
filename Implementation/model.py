
# from  ultralytics import yolo


# class train_model ():
#     def __init__(self,main_obj):
#         self.main_obj = main_obj
#         self.train_model(self)


#     def train_model(self):
#         model = YOLO("yolov8n.pt")  # 'yolov8n.pt' is for Nano, 'yolov8s.pt' is for Small, etc.

#         # Train the model
#         results = model.train(
#             data=self.main_obj.yaml_path,  # Path to YAML configuration file
#             epochs=50,                              # Number of training epochs
#             imgsz=640,                              # Image size
#             batch=16,                               # Batch size
#             name="tumor_detection_model"             # Model name for saving
#         )

#         print("Training complete.")
# from ultralytics import YOLO

# class TrainModel:
#     def __init__(self, main_obj, ui_callback=None):
#         self.main_obj = main_obj
#         self.ui_callback = ui_callback  # Optional callback to update UI

#     def train_model(self, learning_rate, batch_size, epochs, momentum, weight_decay, conf_threshold, nms_threshold):
#         # Initialize YOLO model
#         model = YOLO("yolov8n.pt")

#         # Run YOLOv8 training with additional hyperparameters
#         results = model.train(
#             data=self.main_obj.yaml_path,  # Path to YAML file
#             epochs=epochs,                 # Number of training epochs
#             imgsz=640,                     # Image size
#             batch=batch_size,              # Batch size
#             lr0=learning_rate,             # Learning rate
#             momentum=momentum,             # Momentum
#             weight_decay=weight_decay,     # Weight decay (L2 regularization)
#             conf=conf_threshold,           # Confidence threshold
#             iou=nms_threshold,             # NMS threshold
#             name="tumor_detection_model"
#         )

#         print("Training complete.")


#         # Notify completion and pass results back to UI if needed
#         if self.ui_callback:
#             self.ui_callback("Training complete.")
#         print("Training complete.")


from ultralytics import YOLO

class TrainModel:
    def __init__(self, main_obj, ui_callback=None):
        self.main_obj = main_obj
        self.ui_callback = ui_callback  # Optional callback to update UI

    def train_model(self, learning_rate, batch_size, epochs, conf_threshold, nms_threshold, momentum, weight_decay):
        # Initialize YOLO model
        model = YOLO("yolov8n.pt")

        # Run YOLOv8 training with additional hyperparameters
        results = model.train(
            data=self.main_obj.yaml_path,  # Path to YAML file
            epochs=epochs,                 # Number of training epochs
            imgsz=139,                     # Image size
            batch=batch_size,              # Batch size
            lr0=learning_rate,             # Learning rate
            momentum=momentum,             # Momentum
            weight_decay=weight_decay,     # Weight decay (L2 regularization)
            conf=conf_threshold,           # Confidence threshold
            iou=nms_threshold,             # NMS threshold
            name="tumor_detection_model"
        )

        print("Training complete.")

        # Notify completion and pass results back to UI if needed
        # if self.ui_callback:
        #     self.ui_callback("Training complete.")
