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
        # self.model = TrainModel(master)
        self.create_widget()

    # 
    def create_widget(self):
    # Create a parent frame to center the widgets
        self.center_frame = tk.Frame(self)
        self.center_frame.pack(expand=True)  # expand will center the frame both horizontally and vertically

        # Back Button
        tk.Button(self.center_frame, text="Back", command=self.show_train_frame).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Hyperparameter settings title
        tk.Label(self.center_frame, text="Hyperparameter Tuning", font=("Arial", 14)).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Learning Rate
        tk.Label(self.center_frame, text="Learning Rate:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.learning_rate = tk.DoubleVar(value=0.001)
        tk.Entry(self.center_frame, textvariable=self.learning_rate).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Batch Size
        tk.Label(self.center_frame, text="Batch Size:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.batch_size = tk.IntVar(value=8)
        tk.Entry(self.center_frame, textvariable=self.batch_size).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Epochs
        tk.Label(self.center_frame, text="Epochs:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.epochs = tk.IntVar(value=10)
        tk.Entry(self.center_frame, textvariable=self.epochs).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Confidence Threshold
        tk.Label(self.center_frame, text="Confidence Threshold:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.conf_threshold = tk.DoubleVar(value=0.5)
        tk.Entry(self.center_frame, textvariable=self.conf_threshold).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # NMS Threshold
        tk.Label(self.center_frame, text="NMS Threshold:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.nms_threshold = tk.DoubleVar(value=0.4)
        tk.Entry(self.center_frame, textvariable=self.nms_threshold).grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Momentum
        tk.Label(self.center_frame, text="Momentum:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.momentum = tk.DoubleVar(value=0.937)
        tk.Entry(self.center_frame, textvariable=self.momentum).grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # Weight Decay
        tk.Label(self.center_frame, text="Weight Decay:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.weight_decay = tk.DoubleVar(value=0.0005)
        tk.Entry(self.center_frame, textvariable=self.weight_decay).grid(row=8, column=1, padx=5, pady=5, sticky="w")

        # Training Progress title
        tk.Label(self.center_frame, text="Training Progress", font=("Arial", 14)).grid(row=9, column=0, columnspan=2, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.center_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        
        # Start Training Button
        self.start_button = tk.Button(self.center_frame, text="Start Training", command=self.start_training)
        self.start_button.grid(row=11, column=0, padx=10, pady=10, sticky="e")
        
        # Save Model Button
        self.save_button = tk.Button(self.center_frame, text="Save Model", command=self.save_model, state=tk.DISABLED)
        self.save_button.grid(row=11, column=1, padx=10, pady=10, sticky="w")


    def start_training(self):
        pass

    def save_model(self):
        pass

        # # Matplotlib figure for accuracy and loss
        # self.fig, (self.ax_acc, self.ax_loss) = plt.subplots(2, 1, figsize=(5, 5))
        # self.ax_acc.set_title("Accuracy over Epochs")
        # self.ax_loss.set_title("Loss over Epochs")
        # self.ax_acc.set_ylabel("Accuracy")
        # self.ax_loss.set_ylabel("Loss")
        # self.ax_loss.set_xlabel("Epoch")

        # self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        # self.canvas.get_tk_widget().grid(pady=10)

        # # For storing metric data
        # self.train_accuracy_data = []
        # self.train_loss_data = []

    # def start_training(self):
    #     self.model.train_model(
    #         learning_rate=self.learning_rate.get(),
    #         batch_size=self.batch_size.get(),
    #         epochs=self.epochs.get(),
    #         conf_threshold=self.conf_threshold.get(),
    #         nms_threshold=self.nms_threshold.get(),
    #         momentum=self.momentum.get(),
    #         weight_decay=self.weight_decay.get()
    #     )

    # def start_training(self):
    #     """Simulate model training with real-time progress and metrics update."""
    #     self.progress["value"] = 0
    #     max_value = self.epochs.get() * 10  # Simulated steps per epoch
    #     self.progress["maximum"] = max_value

    #     # Reset data for a new training session
    #     self.train_accuracy_data.clear()
    #     self.train_loss_data.clear()
        
    #     self.ax_acc.clear()
    #     self.ax_loss.clear()
    #     self.ax_acc.set_title("Accuracy over Epochs")
    #     self.ax_loss.set_title("Loss over Epochs")
        
    #     self.start_button["state"] = tk.DISABLED
    #     self.save_button["state"] = tk.DISABLED

        # # Simulated training loop
        # for step in range(1, max_value + 1):
        #     # Update progress bar
        #     self.progress["value"] = step
        #     self.update_training_metrics(step, max_value)
        #     self.update_validation_metrics(step, max_value)
        #     self.plot_metrics(step // 10)  # Plot metrics per epoch
        #     self.update_idletasks()
        #     time.sleep(0.1)  # Simulate training time for each step

        # messagebox.showinfo("Training Complete", "Model training is complete!")
        # self.start_button["state"] = tk.NORMAL
        # self.save_button["state"] = tk.NORMAL

    # def update_training_metrics(self, step, max_steps):
    #     # Simulated accuracy and loss
    #     accuracy = round(random.uniform(0.8, 1.0), 4)
    #     loss = round(random.uniform(0.1, 0.5), 4)
        
    #     # Store for plotting
    #     if step % 10 == 0:
    #         self.train_accuracy_data.append(accuracy)
    #         self.train_loss_data.append(loss)

    # def update_validation_metrics(self, step, max_steps):
    #     # Simulated validation metrics (adjust as needed for real metrics)
    #     val_accuracy = round(random.uniform(0.75, 0.95), 4)
    #     val_loss = round(random.uniform(0.15, 0.45), 4)

    # def plot_metrics(self, epoch):
    #     # Plot updated data on matplotlib figure
    #     self.ax_acc.clear()  # Clear old plot
    #     self.ax_loss.clear()  # Clear old plot
        
    #     self.ax_acc.plot(range(1, epoch + 1), self.train_accuracy_data, label="Training Accuracy", color="b")
    #     self.ax_loss.plot(range(1, epoch + 1), self.train_loss_data, label="Training Loss", color="r")
        
    #     # Refresh the canvas to display updated charts
    #     self.ax_acc.set_title("Accuracy over Epochs")
    #     self.ax_loss.set_title("Loss over Epochs")
    #     self.ax_acc.set_ylabel("Accuracy")
    #     self.ax_loss.set_ylabel("Loss")
    #     self.ax_loss.set_xlabel("Epoch")
    #     self.canvas.draw()

