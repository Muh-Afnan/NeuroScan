import tkinter as tk
from tkinter import ttk, messagebox
import os, json
import re
import seaborn as sns
import numpy as np
from Implementation.model import TrainModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics import confusion_matrix, precision_recall_curve, f1_score
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
        self.output_canvas = tk.Canvas(self.left_frame, width=667, height = 500 )
        self.output_canvas.pack(pady=20)
        # Dropdown to select metric
        self.metric_option = tk.StringVar(value="Select Metric")
        self.metric_dropdown = ttk.OptionMenu(
            self.left_frame, self.metric_option, "Select Metric",
            "Confusion Matrix", "F1 Curve", "PR Curve", "P Curve", "R Curve",
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
        self.conf_threshold = tk.DoubleVar(value=0.5)
        tk.Entry(right_frame, textvariable=self.conf_threshold).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # NMS Threshold
        tk.Label(right_frame, text="NMS Threshold:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.nms_threshold = tk.DoubleVar(value=0.4)
        tk.Entry(right_frame, textvariable=self.nms_threshold).grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Momentum
        tk.Label(right_frame, text="Momentum:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.momentum = tk.DoubleVar(value=0.937)
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
    
    # def latest_model(self):
    #     self.metrices_path = "D:/Project/NeuroScan/runs/detect"
        
    #     # Check if the path exists
    #     if not os.path.exists(self.metrices_path):
    #         print(f"Error: The path {self.metrices_path} does not exist.")
    #         return None
        
    #     # List all subdirectories inside the 'detect' folder
    #     all_folders = [f for f in os.listdir(self.metrices_path) if os.path.isdir(os.path.join(self.metrices_path, f))]
        
    #     # Sort the folders based on the numeric value at the end of the folder name
    #     def extract_numeric_part(folder_name):
    #         match = re.search(r'(\d+)$', folder_name)
    #         return int(match.group(1)) if match else 0
        
    #     all_folders.sort(key=extract_numeric_part)
        
    #     if all_folders:
    #         # Get the most recent model folder (the last one after sorting)
    #         latest_folder = all_folders[-1]
    #         return os.path.join(self.metrices_path, latest_folder)
    #     return None

    # def show_metrices(self, selected_metric):
    #     raw_path = self.latest_model()
    #     if not raw_path:
    #         messagebox.showerror("Error", "No model found.")
    #         return
    #     else:
    #         if selected_metric == "Confusion Matrix":
    #             self.output_canvas.delete("all")
    #             # Load the metric image using PIL
    #             metric_path = os.path.normpath(os.path.join(raw_path, "confusion_matrix.png")).replace("\\", "/")
    #             if os.path.exists(metric_path):
    #                 metric_image = Image.open(metric_path)  # Open the image using PIL
    #                 metric_image = metric_image.resize((667, 500), Image.Resampling.LANCZOS)
    #                 metric_image = ImageTk.PhotoImage(metric_image)  # Convert to Tkinter-compatible image
    #                 self.output_canvas.create_image(0,0,anchor = "nw",image = metric_image)
    #                 self.output_canvas.image = metric_image
    #             else:
    #                 messagebox.showerror("Error", "Confusion Matrix image not found.")
    
    def _embed_plot(self, figure):
        for widget in self.output_canvas.winfo_children():
            widget.destroy()

        figure.set_size_inches(6, 4)
        canvas = FigureCanvasTkAgg(figure, master=self.output_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas_widget.config(width=600, height=400)
        canvas.draw()
    
    def show_metrices(self, selected_metric):
        # raw_path = self.latest_model()
        if not self.master.metrices_path:
            messagebox.showerror("Error", "No model found.")
            return
        else:
            if selected_metric == "Confusion Matrix":
                self.output_canvas.delete("all")
                self.plot_confusion_matrix()
            elif selected_metric == "F1 Curve":
                self.output_canvas.delete("all")
                self.f1_curve()
            elif selected_metric == "PR Curve":
                self.output_canvas.delete("all")
                self.precision_recall_plot()
            elif selected_metric == "P Curve":
                self.output_canvas.delete("all")
                self.plot_precision_curve()
            elif selected_metric == "R Curve":
                self.output_canvas.delete("all")
                self.plot_recall_curve()
    
    def load_data(self):
        with open(self.master.metrices_path, 'r') as json_file:
            curves_data = json.load(json_file)
        
        
        self.precision_recall = curves_data['Precision-Recall']
        self.f1_confidence = curves_data['F1-Confidence']
        self.precision_confidence = curves_data['Precision-Confidence']
        self.recall_confidence = curves_data['Recall-Confidence']

    def precision_recall_plot(self):
        self.load_data()

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(self.precision_recall, self.f1_confidence, label='F1-Confidence(B)')
        ax.plot(self.precision_recall, self.precision_confidence, label='Precision-Confidence(B)')
        ax.plot(self.precision_recall, self.recall_confidence, label='Recall-Confidence(B)')

        ax.set_xlabel('Threshold')
        ax.set_ylabel('Score')
        ax.set_title('Precision-Recall Curves')
        ax.legend(loc='best')
        ax.grid(True)

        self._embed_plot(fig)

    def f1_curve(self):
        self.load_data()
        precision = self.precision_confidence
        recall = self.recall_confidence
        thresholds = self.precision_recall
        
        # Calculate F1 scores for each threshold
        f1_scores = 2 * (np.array(precision) * np.array(recall)) / (np.array(precision) + np.array(recall))
        
        # Handle cases where precision + recall = 0 (avoid division by zero)
        f1_scores = np.nan_to_num(f1_scores, nan=0.0)  # Set NaN to 0

        # Create a plot for the F1 curve
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(thresholds, f1_scores, label='F1 Score')

        ax.set_xlabel('Threshold')
        ax.set_ylabel('F1 Score')
        ax.set_title('F1 Score vs Threshold')
        ax.legend(loc='best')
        ax.grid(True)

        self._embed_plot(fig) 

    def plot_confusion_matrix(self):
        self.load_data()

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot the precision, recall, and F1 confidence scores at different thresholds
        ax.plot(self.precision_recall, self.f1_confidence, label='F1-Confidence')
        ax.plot(self.precision_recall, self.precision_confidence, label='Precision-Confidence')
        ax.plot(self.precision_recall, self.recall_confidence, label='Recall-Confidence')

        # Set labels and title for the plot
        ax.set_xlabel('Threshold')
        ax.set_ylabel('Score')
        ax.set_title('Precision-Recall Curves')
        
        # Show a legend and grid
        ax.legend(loc='best')
        ax.grid(True)

        # Display the plot
        self._embed_plot(fig)

    

    # def plot_confusion_matrix(self):
    #     self.load_data()
    #     cm = confusion_matrix(self.y_true, self.y_pred)
    #     fig, ax = plt.subplots()
    #     cax = ax.matshow(cm, cmap='Blues')
    #     fig.colorbar(cax)
    #     ax.set_xlabel('Predicted')
    #     ax.set_ylabel('True')
    #     ax.set_title('Confusion Matrix')
    #     self._embed_plot(fig)

    # def plot_precision_recall_curve(self):
    #     precision, recall, _ = precision_recall_curve(self.y_true, self.y_pred)
        
    #     plt.plot(recall, precision, marker='.', label='Precision-Recall curve')
    #     plt.xlabel('Recall')
    #     plt.ylabel('Precision')
    #     plt.title('Precision-Recall Curve')
    #     plt.legend()
    #     self._embed_plot(plt.gcf())
    
    # def plot_f1_score_curve(self):
    #     precision, recall, _ = precision_recall_curve(self.y_true, self.y_pred)
    #     f1_scores = 2 * (precision * recall) / (precision + recall)
        
    #     plt.plot(recall, f1_scores, marker='.', label='F1 Score Curve')
    #     plt.xlabel('Recall')
    #     plt.ylabel('F1 Score')
    #     plt.title('F1 Score Curve')
    #     plt.legend()
    #     self._embed_plot(plt.gcf())
    
    # def plot_precision_curve(self):
    #     precision, _, _ = precision_recall_curve(self.y_true, self.y_pred)
        
    #     plt.plot(precision, label='Precision Curve')
    #     plt.xlabel('Threshold')
    #     plt.ylabel('Precision')
    #     plt.title('Precision Curve')
    #     plt.legend()
    #     self._embed_plot(plt.gcf())
    
    # def plot_recall_curve(self):
    #     _, recall, _ = precision_recall_curve(self.y_true, self.y_pred)
        
    #     plt.plot(recall, label='Recall Curve')
    #     plt.xlabel('Threshold')
    #     plt.ylabel('Recall')
    #     plt.title('Recall Curve')
    #     plt.legend()
    #     self._embed_plot(plt.gcf())

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