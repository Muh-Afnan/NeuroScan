import tkinter as tk
from tkinter import ttk, messagebox
import os, json
import re
import seaborn as sns
import numpy as np
from Implementation.model import TrainModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from sklearn.metrics import confusion_matrix, precision_recall_curve, f1_score
from PIL import Image, ImageTk

class modeltrainingscreen(tk.Frame):
    def __init__(self, master, show_train_frame):
        super().__init__(master)
        self.master = master
        self.dataset_path = self.master.dataset_path
        self.show_train_frame = show_train_frame
        self.yolomodel = TrainModel(self.master)
        self.y_true = self.yolomodel.y_true
        self.y_pred = self.yolomodel.y_pred
        self.create_widget()

    def create_widget(self):
        # Split the UI into two frames: Left for Canvas, Right for Controls
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Back Button at the top right
        back_button = tk.Button(right_frame, text="Back", command=self.show_train_frame)
        back_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # Left Frame: Output Canvas and Dropdown
        # self.figure, self.ax = plt.subplots()  # Initialize figure and axis
        self.output_canvas = tk.Canvas(self.left_frame, width=667, height = 500,borderwidth=1)
        self.output_canvas.pack(pady=20)
        # Dropdown to select metric
        self.metric_option = tk.StringVar(value="Select Metric")
        self.metric_dropdown = ttk.OptionMenu(
            self.left_frame, self.metric_option, "Select Metric",
            "Confusion Matrix","F1 Curve", "P Curve", "R_curve","PR Curve",
            command=self.show_metrices  # Callback to update canvas
        )
        self.metric_dropdown.pack(pady=10)
        

        # Right Frame: Hyperparameter Tuning Section
        tk.Label(right_frame, text="Hyperparameter Tuning", font=("Arial", 14)).grid(row=1, column=0, columnspan=2, pady=10)

        # Learning Rate
        tk.Label(right_frame, text="Learning Rate:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.learning_rate = tk.DoubleVar(value=0.001)
        tk.Entry(right_frame, textvariable=self.learning_rate).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Batch Size
        tk.Label(right_frame, text="Batch Size:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.batch_size = tk.IntVar(value=8)
        tk.Entry(right_frame, textvariable=self.batch_size).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Epochs
        tk.Label(right_frame, text="Epochs:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.epochs = tk.IntVar(value=10)
        tk.Entry(right_frame, textvariable=self.epochs).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Confidence Threshold
        tk.Label(right_frame, text="Confidence Threshold:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.conf_threshold = tk.DoubleVar(value=0.4)
        tk.Entry(right_frame, textvariable=self.conf_threshold).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # NMS Threshold
        tk.Label(right_frame, text="NMS Threshold:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.nms_threshold = tk.DoubleVar(value=0.4)
        tk.Entry(right_frame, textvariable=self.nms_threshold).grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Momentum
        tk.Label(right_frame, text="Momentum:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.momentum = tk.DoubleVar(value=0.9)
        tk.Entry(right_frame, textvariable=self.momentum).grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # Weight Decay
        tk.Label(right_frame, text="Weight Decay:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.weight_decay = tk.DoubleVar(value=0.0005)
        tk.Entry(right_frame, textvariable=self.weight_decay).grid(row=8, column=1, padx=5, pady=5, sticky="w")

        # Training Progress title
        tk.Label(right_frame, text="Training Progress", font=("Arial", 14)).grid(row=9, column=0, columnspan=2, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(right_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        # Start Training Button
        self.start_button = tk.Button(right_frame, text="Start Training", command=self.start_training)
        self.start_button.grid(row=11, column=0, padx=10, pady=10, sticky="e")

        # Save Model Button
        self.save_button = tk.Button(right_frame, text="Save Model", command=self.save_model)
        self.save_button.grid(row=11, column=1, padx=10, pady=10, sticky="w")
    
    def latest_model(self):
        self.metrices_path = self.master.metrices_path
        
        # Check if the path exists
        if not os.path.exists(self.metrices_path):
            print(f"Error: The path {self.metrices_path} does not exist.")
            return None
        
        # List all subdirectories inside the 'detect' folder
        all_folders = [f for f in os.listdir(self.metrices_path) if os.path.isdir(os.path.join(self.metrices_path, f))]
        
        # Sort the folders based on the numeric value at the end of the folder name
        def extract_numeric_part(folder_name):
            match = re.search(r'(\d+)$', folder_name)
            return int(match.group(1)) if match else 0
        
        all_folders.sort(key=extract_numeric_part)
        
        if all_folders:
            # Get the most recent model folder (the last one after sorting)
            latest_folder = all_folders[-1]
            return os.path.join(self.metrices_path, latest_folder)
        return None

    def canvas_plot(self, plot):
        self.output_canvas.delete("all")
        # Load the metric image using PIL
        metric_path = os.path.normpath(os.path.join(self.raw_path, plot)).replace("\\", "/")
        if os.path.exists(metric_path):
            metric_image = Image.open(metric_path)  # Open the image using PIL
            metric_image = metric_image.resize((667, 500), Image.Resampling.LANCZOS)
            metric_image = ImageTk.PhotoImage(metric_image)  # Convert to Tkinter-compatible image
            self.output_canvas.create_image(0,0,anchor = "nw",image = metric_image)
            self.output_canvas.image = metric_image
        else:
            messagebox.showerror("Error", "Confusion Matrix image not found.")

    def show_metrices(self, selected_metric):
        self.raw_path = self.latest_model()
        if not self.raw_path:
            messagebox.showerror("Error", "No model found.")
            return
        else:
            if selected_metric == "Confusion Matrix":
                self.canvas_plot("confusion_matrix.png")
            elif selected_metric == "F1 Curve":
                self.canvas_plot("F1_curve.png")
            elif selected_metric == "P Curve":
                self.canvas_plot("P_curve.png")
            elif selected_metric == "PR Curve":
                self.canvas_plot("PR_curve.png")
            elif selected_metric == "R Curve":
                self.canvas_plot("R_curve.png")
            else:
                return

    def start_training(self):
        epochs = self.epochs.get()
        batch_size = self.batch_size.get()
        lr0 = self.learning_rate.get()
        momentum = self.momentum.get()
        weight_decay = self.weight_decay.get()
        conf = self.conf_threshold.get()
        iou = self.nms_threshold.get()
        
        # Start training
        self.yolomodel.train_model(epochs, batch_size, lr0, momentum, weight_decay, conf, iou)

    def save_model(self):
        self.yolomodel.save_model()