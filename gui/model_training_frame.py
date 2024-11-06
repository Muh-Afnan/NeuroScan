import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class TrainModelScreen(tk.Toplevel):
    def __init__(self, master, main_obj):
        super().__init__(master)
        self.main_obj = main_obj
        self.title("Train YOLO Model")
        self.geometry("700x700")
        
        # Hyperparameter settings
        tk.Label(self, text="Hyperparameter Tuning", font=("Arial", 14)).pack(pady=10)
        
        # Learning Rate
        tk.Label(self, text="Learning Rate:").pack(pady=5)
        self.learning_rate = tk.DoubleVar(value=0.001)
        tk.Entry(self, textvariable=self.learning_rate).pack(pady=5)
        
        # Batch Size
        tk.Label(self, text="Batch Size:").pack(pady=5)
        self.batch_size = tk.IntVar(value=8)
        tk.Entry(self, textvariable=self.batch_size).pack(pady=5)
        
        # Epochs
        tk.Label(self, text="Epochs:").pack(pady=5)
        self.epochs = tk.IntVar(value=10)
        tk.Entry(self, textvariable=self.epochs).pack(pady=5)
        
        # Confidence Threshold
        tk.Label(self, text="Confidence Threshold:").pack(pady=5)
        self.conf_threshold = tk.DoubleVar(value=0.5)
        tk.Entry(self, textvariable=self.conf_threshold).pack(pady=5)
        
        # NMS Threshold
        tk.Label(self, text="NMS Threshold:").pack(pady=5)
        self.nms_threshold = tk.DoubleVar(value=0.4)
        tk.Entry(self, textvariable=self.nms_threshold).pack(pady=5)

        # Progress bar
        tk.Label(self, text="Training Progress", font=("Arial", 14)).pack(pady=10)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        
        # Start Training Button
        self.start_button = tk.Button(self, text="Start Training", command=self.start_training)
        self.start_button.pack(pady=10)
        
        # Save Model Button
        self.save_button = tk.Button(self, text="Save Model", command=self.save_model, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        # Matplotlib figure for accuracy and loss
        self.fig, (self.ax_acc, self.ax_loss) = plt.subplots(2, 1, figsize=(5, 5))
        self.ax_acc.set_title("Accuracy over Epochs")
        self.ax_loss.set_title("Loss over Epochs")
        self.ax_acc.set_ylabel("Accuracy")
        self.ax_loss.set_ylabel("Loss")
        self.ax_loss.set_xlabel("Epoch")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)

        # For storing metric data
        self.accuracy_data = []
        self.loss_data = []

    def start_training(self):
        """Simulate model training with real-time progress and metrics update."""
        self.progress["value"] = 0
        max_value = self.epochs.get() * 10  # Simulated steps per epoch
        self.progress["maximum"] = max_value

        # Reset data for a new training session
        self.accuracy_data.clear()
        self.loss_data.clear()
        self.ax_acc.clear()
        self.ax_loss.clear()
        self.ax_acc.set_title("Accuracy over Epochs")
        self.ax_loss.set_title("Loss over Epochs")
        
        self.start_button["state"] = tk.DISABLED
        self.save_button["state"] = tk.DISABLED

        # Simulated training loop
        for i in range(1, max_value + 1):
            # Update progress bar
            self.progress["value"] = i
            self.update_training_metrics(i, max_value)
            self.update_validation_metrics(i, max_value)
            self.plot_metrics(i // 10)  # Plot metrics per epoch
            self.update_idletasks()
            self.after(100)

        messagebox.showinfo("Training Complete", "Model training is complete!")
        self.start_button["state"] = tk.NORMAL
        self.save_button["state"] = tk.NORMAL

    def update_training_metrics(self, step, max_steps):
        # Simulated accuracy and loss
        accuracy = round(random.uniform(0.8, 1.0), 4)
        loss = round(random.uniform(0.1, 0.5), 4)
        
        # Store for plotting
        if step % 10 == 0:
            self.accuracy_data.append(accuracy)
            self.loss_data.append(loss)

    def update_validation_metrics(self, step, max_steps):
        # Simulated validation metrics (adjust as needed for real metrics)
        val_accuracy = round(random.uniform(0.75, 0.95), 4)
        val_loss = round(random.uniform(0.15, 0.45), 4)

    def plot_metrics(self, epoch):
        # Plot updated data on matplotlib figure
        self.ax_acc.plot(range(1, epoch + 1), self.accuracy_data, label="Training Accuracy", color="b")
        self.ax_loss.plot(range(1, epoch + 1), self.loss_data, label="Training Loss", color="r")
        
        # Refresh the canvas to display updated charts
        self.canvas.draw()

    def save_model(self):
        try:
            messagebox.showinfo("Save Model", "Model saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Model", f"Failed to save model: {e}")
