import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from Implementation.model import TrainModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class modeltrainingscreen(tk.Frame):
    def __init__(self, master, show_train_frame):
        super().__init__(master)
        self.master = master
        self.dataset_path = self.master.dataset_path
        self.show_train_frame = show_train_frame
        self.yolomodel = TrainModel(self.master)
        self.create_widget()

    def create_widget(self):
        # Split the UI into two frames: Left for Canvas, Right for Controls
        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Left Frame: Output Canvas and Dropdown
        self.output_canvas = FigureCanvasTkAgg(plt.Figure(), master=left_frame)  # Empty canvas initially
        self.output_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Dropdown to select metric
        self.metric_option = tk.StringVar(value="Select Metric")
        self.metric_dropdown = ttk.OptionMenu(
            left_frame, self.metric_option, "Select Metric", 
            "Confusion Matrix", "F1 Curve", "PR Curve", "P Curve", "R Curve",
            command=self.update_canvas  # Callback to update canvas
        )
        self.metric_dropdown.pack(pady=10)

        # Right Frame: Hyperparameter settings and controls
        # (All previous code for hyperparameters input fields goes here in right_frame)
        tk.Label(right_frame, text="Hyperparameter Tuning", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Example parameter, repeat for others
        tk.Label(right_frame, text="Learning Rate:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.learning_rate = tk.DoubleVar(value=0.001)
        tk.Entry(right_frame, textvariable=self.learning_rate).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Progress bar
        self.progress = ttk.Progressbar(right_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=20, column=0, columnspan=2, padx=10, pady=10)

        # Buttons
        self.start_button = tk.Button(right_frame, text="Start Training", command=self.start_training)
        self.start_button.grid(row=21, column=0, padx=10, pady=10, sticky="e")
        
        self.save_button = tk.Button(right_frame, text="Save Model", command=self.save_model)
        self.save_button.grid(row=21, column=1, padx=10, pady=10, sticky="w")

    def update_canvas(self, selected_metric):
        # Logic to update canvas based on selected metric
        plt.clf()  # Clear previous plot
        fig = plt.Figure()
        ax = fig.add_subplot(111)

        if selected_metric == "Confusion Matrix":
            # Generate and display confusion matrix
            ax.imshow(self.yolomodel.get_confusion_matrix(), cmap="Blues")
        elif selected_metric == "F1 Curve":
            # Plot F1 curve
            ax.plot(self.yolomodel.get_f1_curve())
        elif selected_metric == "PR Curve":
            # Plot Precision-Recall curve
            ax.plot(self.yolomodel.get_pr_curve())
        # Add more cases as needed

        self.output_canvas = FigureCanvasTkAgg(fig, master=self.output_canvas.get_tk_widget())
        self.output_canvas.draw()



    def start_training(self):
        epochs = self.epochs.get()
        batch_size = self.batch_size.get()
        lr0=self.learning_rate.get()
        momentum = self.momentum.get()
        weight_decay = self.weight_decay.get()
        conf = self.conf_threshold.get()
        iou = self.nms_threshold.get()
        self.yolomodel.train_model(epochs,batch_size,lr0,momentum,weight_decay,conf,iou)

    def save_model(self):
        self.yolomodel.save_model()
