
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
from ultralytics import YOLO

class TrainModel:
    def __init__(self, main_obj, ui_callback=None):
        self.main_obj = main_obj
        self.ui_callback = ui_callback  # Optional callback to update UI

    def train_model(self, learning_rate, batch_size, epochs):
        # Initialize YOLO model
        model = YOLO("yolov8n.pt")

        # Run YOLOv8 training with parameters from UI
        results = model.train(
            data=self.main_obj.yaml_path,  # Path to YAML file
            epochs=epochs,                 # Number of training epochs
            imgsz=640,                     # Image size
            batch=batch_size,              # Batch size
            lr0=learning_rate,             # Learning rate
            name="tumor_detection_model"
        )

        # Notify completion and pass results back to UI if needed
        if self.ui_callback:
            self.ui_callback("Training complete.")
        print("Training complete.")
