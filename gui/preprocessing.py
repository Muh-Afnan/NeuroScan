import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from preprocessing_logic import backend
import threading


class preprocess(tk.Frame):
    def __init__(self,master,callback_to_train_screen):
        super().__init__(master)
        self.master = master
        # self.dataset_path = master.dataset_path
        self.call_back_train = callback_to_train_screen
         
        self.preprocessing_status = {
            "Normalization": tk.BooleanVar(),
            "Noise Reduction": tk.BooleanVar(),
            "Skull Stripping": tk.BooleanVar(),
            "Artifact Removal": tk.BooleanVar(),
        }

        self.create_widgets()
    
    def create_widgets(self):
        pass
            

    def preprocess_data(self):
            if not self.dataset_path:
                messagebox.showwarning("No Dataset", "Please upload a dataset first.")
                return

            progress_window = tk.Toplevel(self)
            progress_window.title("Preprocessing Progress")
            progress_window.geometry("600x400")

            tk.Label(progress_window, text="Preprocessing images...").pack(pady=10)

        # Create a frame to hold the progress bars and labels
            progress_frame = tk.Frame(progress_window)
            progress_frame.pack(pady=10)

            progress_bars = {}
            for step in self.preprocessing_status:
                tk.Label(progress_frame, text=step).pack(anchor="w", padx=10)
                progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=500, mode="determinate")
                progress_bar.pack(pady=5)
                progress_bars[step] = progress_bar

            def run_preprocessing():
                total_images = len(self.loaded_images)
                for step in self.preprocessing_status:
                    self.preprocessing_status[step].set(True)
                    progress_bars[step]["maximum"] = total_images
                    progress_bars[step]["value"] = 0
                    progress_window.update_idletasks()

                    # Simulate the preprocessing step
                    for idx, (name, img) in enumerate(self.loaded_images):
                        if step == "Normalization":
                            img = backend.preprocess_image(img)
                        # Update progress bar for the current step
                        progress_bars[step]["value"] += 1
                        progress_window.update_idletasks()

                    # Mark the step as complete
                    self.preprocessing_status[step].set(False)

                messagebox.showinfo("Preprocessing", "Preprocessing completed!")
                progress_window.destroy()

            threading.Thread(target=run_preprocessing).start()
            