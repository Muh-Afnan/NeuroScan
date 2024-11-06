
from  ultralytics import yolo


class train_model ():
    def __init__(self,main_obj):
        self.main_obj = main_obj
        self.train_model(self)


    def train_model(self):
        model = YOLO("yolov8n.pt")  # 'yolov8n.pt' is for Nano, 'yolov8s.pt' is for Small, etc.

        # Train the model
        results = model.train(
            data=self.main_obj.yaml_path,  # Path to YAML configuration file
            epochs=50,                              # Number of training epochs
            imgsz=640,                              # Image size
            batch=16,                               # Batch size
            name="tumor_detection_model"             # Model name for saving
        )

        print("Training complete.")