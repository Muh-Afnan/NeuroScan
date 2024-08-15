import tkinter as tk
from tkinter import filedialog, messagebox

class DetectTumorForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.selected_images = []

        self.create_widgets()

    def create_widgets(self):
        self.label_select = tk.Label(self, text="Select CT/MRI Images for Tumor Detection", font=("Arial", 14))
        self.label_select.pack(pady=10)

        self.button_browse = tk.Button(self, text="Browse Images", command=self.browse_images)
        self.button_browse.pack(pady=10)

        self.label_selected = tk.Label(self, text="Selected Images:")
        self.label_selected.pack(pady=10)

        self.listbox_images = tk.Listbox(self, selectmode=tk.MULTIPLE, width=50, height=5)
        self.listbox_images.pack(pady=10)

        self.button_detect = tk.Button(self, text="Detect Tumor", command=self.detect_tumor)
        self.button_detect.pack(pady=10)

        self.button_clear = tk.Button(self, text="Clear Selection", command=self.clear_selection)
        self.button_clear.pack(pady=10)

    def browse_images(self):
        filetypes = (
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif"),
            ("All files", "*.*")
        )
        filenames = filedialog.askopenfilenames(filetypes=filetypes)
        if filenames:
            self.selected_images = list(filenames)
            self.update_image_listbox()

    def update_image_listbox(self):
        self.listbox_images.delete(0, tk.END)
        for image_path in self.selected_images:
            self.listbox_images.insert(tk.END, image_path)

    def detect_tumor(self):
        if not self.selected_images:
            messagebox.showwarning("No Images Selected", "Please select images first.")
            return

        # Placeholder logic for tumor detection using selected images
        # Replace with actual detection logic
        messagebox.showinfo("Tumor Detection", "Detecting tumor in selected images.")

    def clear_selection(self):
        self.selected_images = []
        self.listbox_images.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Detect Tumor")
    app = DetectTumorForm(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
