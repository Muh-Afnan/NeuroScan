import tkinter as tk
from Implementation.model import TrainModel
from PIL import Image, ImageTk
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

        heading_label = tk.Label(self.center_frame, text="Detect Tumor", font=("Arial", 20, "bold"))
        heading_label.pack(pady=(10,5))

        self.back_button = tk.Button(self.center_frame, text="Back", command=self.callback_mainscreen)
        self.back_button.pack()

        self.canvas = tk.Canvas(self.center_frame, width= 139*2, height = 132*2)
        self.canvas.pack(pady=10)

        self.result_label = tk.Label(self.center_frame,text = "Select your Image", font = ("Arial",14))
        self.result_label.pack(pady=(5,15))

        self.button_frame = tk.Frame(self.center_frame)
        self.button_frame.pack(pady=(10,20))

        self.clear_button = tk.Button(self.button_frame, text = "Clear", command = self.clear_image)
        self.clear_button.grid(row=0, column=0, padx=5)

        self.selectimage = tk.Button(self.button_frame, text="Select Image", command=self.select_image)
        self.selectimage.grid(row=0, column=1, padx=5)

        self.predict = tk.Button(self.button_frame, text="Check Tumor", command=self.display_detection)
        self.predict.grid(row=0, column=2, padx=5)

    def select_image(self):
        image_file = tk.filedialog.askopenfilename(title="Select Image for Tumor Detection")
        if image_file:
            self.main_obj.detect_tumor = image_file
            image = cv2.imread(image_file)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            pil_image = pil_image.resize(((139*2),(132*2)))
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.canvas.create_image(0,0, anchor = tk.NW, image=self.tk_image)
            self.result_label.config(text="Image Selected")

    def clear_image(self):
        self.canvas.delete("all")
        self.result_label.config(text = "Select your Image")
        self.main_obj.detect_tumor_image = None


    def display_detection(self):
        model = TrainModel(self.main_obj)
        image = model.predict()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        # Convert image to a Tkinter-compatible format
        pil_image = Image.fromarray(image_rgb)
        pil_image = pil_image.resize(((139*2),(132*2)))
        tk_image = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image  # Keep a reference
