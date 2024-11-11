import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Implementation.model import TrainModel
import matplotlib.pyplot as plt

class modeltrainingscreen(tk.Frame):
    def __init__(self, master, show_train_frame):
        super().__init__(master)
        self.master = master
        self.dataset_path = self.master.dataset_path
        self.show_train_frame = show_train_frame
        self.create_widget()
        self.train_model_instance = TrainModel(main_obj=self.master, ui_callback=self.training_complete_callback)


    def create_widget(self):
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        tk.Button(self.left_frame, text="Back", command=self.show_train_frame).grid(pady=5)
        
        # Hyperparameter settings
        tk.Label(self.left_frame, text="Hyperparameter Tuning", font=("Arial", 14)).grid(pady=10)

        # Learning Rate
        tk.Label(self.left_frame, text="Learning Rate:").grid(pady=5)
        self.learning_rate = tk.DoubleVar(value=0.001)
        tk.Entry(self.left_frame, textvariable=self.learning_rate).grid(pady=5)

        # Batch Size
        tk.Label(self.left_frame, text="Batch Size:").grid(pady=5)
        self.batch_size = tk.IntVar(value=8)
        tk.Entry(self.left_frame, textvariable=self.batch_size).grid(pady=5)

        # Epochs
        tk.Label(self.left_frame, text="Epochs:").grid(pady=5)
        self.epochs = tk.IntVar(value=10)
        tk.Entry(self.left_frame, textvariable=self.epochs).grid(pady=5)

        # Confidence Threshold
        tk.Label(self.left_frame, text="Confidence Threshold:").grid(pady=5)
        self.conf_threshold = tk.DoubleVar(value=0.5)
        tk.Entry(self.left_frame, textvariable=self.conf_threshold).grid(pady=5)

        # NMS Threshold
        tk.Label(self.left_frame, text="NMS Threshold:").grid(pady=5)
        self.nms_threshold = tk.DoubleVar(value=0.4)
        tk.Entry(self.left_frame, textvariable=self.nms_threshold).grid(pady=5)

        # Progress bar
        tk.Label(self.right_frame, text="Training Progress", font=("Arial", 14)).grid(pady=10)
        self.progress = ttk.Progressbar(self.right_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(pady=10)

        # Start Training Button
        self.start_button = tk.Button(self.right_frame, text="Start Training", command=self.start_training)
        self.start_button.grid(pady=10)

        # Save Model Button
        self.save_button = tk.Button(self.left_frame, text="Save Model", command=self.save_model, state=tk.DISABLED)
        self.save_button.grid(pady=10)

        # Matplotlib figure for accuracy and loss
        self.fig, (self.ax_acc, self.ax_loss) = plt.subplots(2, 1, figsize=(5, 5))
        self.ax_acc.set_title("Accuracy over Epochs")
        self.ax_loss.set_title("Loss over Epochs")
        self.ax_acc.set_ylabel("Accuracy")
        self.ax_loss.set_ylabel("Loss")
        self.ax_loss.set_xlabel("Epoch")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().grid(pady=10)

        # For storing metric data
        self.train_accuracy_data = []
        self.train_loss_data = []

    def start_training(self):
        """Simulate model training with real-time progress and metrics update."""
        self.progress["value"] = 0
        max_value = self.epochs.get() * 10  # Simulated steps per epoch
        self.progress["maximum"] = max_value

        # Reset data for a new training session
        self.train_accuracy_data.clear()
        self.train_loss_data.clear()
        
        self.ax_acc.clear()
        self.ax_loss.clear()
        self.ax_acc.set_title("Accuracy over Epochs")
        self.ax_loss.set_title("Loss over Epochs")
        
        self.start_button["state"] = tk.DISABLED
        self.save_button["state"] = tk.DISABLED

        # Simulated training loop
        for step in range(1, max_value + 1):
            # Update progress bar
            self.progress["value"] = step
            self.update_training_metrics(step, max_value)
            self.update_validation_metrics(step, max_value)
            self.plot_metrics(step // 10)  # Plot metrics per epoch
            self.update_idletasks()
            time.sleep(0.1)  # Simulate training time for each step

        messagebox.showinfo("Training Complete", "Model training is complete!")
        self.start_button["state"] = tk.NORMAL
        self.save_button["state"] = tk.NORMAL

    def update_training_metrics(self, step, max_steps):
        # Simulated accuracy and loss
        accuracy = round(random.uniform(0.8, 1.0), 4)
        loss = round(random.uniform(0.1, 0.5), 4)
        
        # Store for plotting
        if step % 10 == 0:
            self.train_accuracy_data.append(accuracy)
            self.train_loss_data.append(loss)

    def update_validation_metrics(self, step, max_steps):
        # Simulated validation metrics (adjust as needed for real metrics)
        val_accuracy = round(random.uniform(0.75, 0.95), 4)
        val_loss = round(random.uniform(0.15, 0.45), 4)

    def plot_metrics(self, epoch):
        # Plot updated data on matplotlib figure
        self.ax_acc.clear()  # Clear old plot
        self.ax_loss.clear()  # Clear old plot
        
        self.ax_acc.plot(range(1, epoch + 1), self.train_accuracy_data, label="Training Accuracy", color="b")
        self.ax_loss.plot(range(1, epoch + 1), self.train_loss_data, label="Training Loss", color="r")
        
        # Refresh the canvas to display updated charts
        self.ax_acc.set_title("Accuracy over Epochs")
        self.ax_loss.set_title("Loss over Epochs")
        self.ax_acc.set_ylabel("Accuracy")
        self.ax_loss.set_ylabel("Loss")
        self.ax_loss.set_xlabel("Epoch")
        self.canvas.draw()

    def save_model(self):
        try:
            # This would be where you'd actually save your model in a real case.
            # Example: model.save('your_model.h5')
            messagebox.showinfo("Save Model", "Model saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Model", f"Failed to save model: {e}")
