import tkinter as tk

class DetectTumor(tk.frame):
    def __init__(self, main_obj,show_main_screen):
        super().__init__(main_obj)
        self.main_obj = main_obj
        self.callback_mainscreen = show_main_screen
        self.create_weidgets()

    def create_weidgets(self):
        self.back_button = tk.Button(self, text="Back", command=self.show_main_screen)
        self.back_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.load_dataset = tk.Button(self, text="Select Image", command=self.select_image)
        self.load_dataset.grid(row=3, column=0, padx=10, pady=10)

        self.predict = tk.Button(self, text="Check Tumor", command=self.check_tumor)
        self.load_dataset.grid(row=3, column=0, padx=10, pady=10)

    def select_image(self):
        image_file = tk.filedialog.askopenfile(title="Select Image for Tumor Detection")
        self.main_obj.detect_tumor = image_file

    def check_tumor(self):
        pass