import tkinter as tk
from Implementation.model import TrainModel
from PIL import ImageTk
import cv2 as cv2

class DetectTumor(tk.Frame):
    def __init__(self, main_obj,show_main_screen):
        super().__init__(main_obj)
        self.main_obj = main_obj
        self.callback_mainscreen = show_main_screen
        self.create_weidgets()

    def create_weidgets(self):
        self.center_frame = tk.Frame(self)
        self.center_frame.pack(expand=True)
        self.back_button = tk.Button(self.center_frame, text="Back", command=self.callback_mainscreen)
        self.back_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.selectimage = tk.Button(self.center_frame, text="Select Image", command=self.select_image)
        self.selectimage.grid(row=2, column=1, padx=10, pady=10)

        self.predict = tk.Button(self.center_frame, text="Check Tumor", command=self.display_detection)
        self.predict.grid(row=3, column=0, padx=10, pady=10)

    def select_image(self):
        image_file = tk.filedialog.askopenfile(title="Select Image for Tumor Detection")
        self.main_obj.detect_tumor = image_file

    def display_detection(self):
        model = TrainModel(self.main_obj)
        image_rgb, results, lables = model.predict()
        tk_image = ImageTk.PhotoImage(image=cv2.cvtColor(image_rgb, cv2.COLOR_RGB2RGBA))

        canvas = tk.Canvas(self.center_frame, width=image_rgb.width, height=image_rgb.height)
        canvas.pack()
         # Display image on canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image  # Keep a reference to prevent garbage collection


        # Check if results have any bounding boxes
        if results and hasattr(results, 'boxes'):
            for result in results:
                # Extract bounding box and label
                x, y, w, h = result['bounding_box']
                confidence = result['confidence']
                label_index = result['label']
                label_text = f"{lables[label_index]}: {confidence:.2f}"

                # Draw bounding box on canvas
                canvas.create_rectangle(x, y, x + w, y + h, outline="red", width=2)
                canvas.create_text(x, y - 10, anchor=tk.NW, text=label_text, fill="red", font=("Arial", 10, "bold"))
        else:
            # If no bounding box found, display a message
            canvas.create_text(
                tk_image.width() / 2,
                tk_image.height() / 2,
                text="No Tumor Detected",
                fill="green",
                font=("Arial", 20, "bold")
            )


        