import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2

class GrayscaleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Grayscale Converter")
        self.root.geometry("700x500")

        # Variables to store images
        self.original_image = None  # OpenCV image (numpy array)
        self.display_image = None   # Tkinter PhotoImage to show on canvas

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        load_btn = ttk.Button(btn_frame, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5)

        gray_btn = ttk.Button(btn_frame, text="Apply Grayscale", command=self.apply_grayscale)
        gray_btn.pack(side=tk.LEFT, padx=5)

        # Canvas to display image
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="gray")
        self.canvas.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            # Read image with OpenCV and convert BGR to RGB
            img = cv2.imread(file_path)
            if img is None:
                messagebox.showerror("Error", "Failed to load image.")
                return

            self.original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.show_image(self.original_image)

    def show_image(self, img):
        # Resize image to fit canvas while maintaining aspect ratio
        canvas_w, canvas_h = 600, 400
        h, w = img.shape[:2]
        scale = min(canvas_w / w, canvas_h / h)
        new_w, new_h = int(w * scale), int(h * scale)

        resized_img = cv2.resize(img, (new_w, new_h))

        # Convert to PIL image and then to PhotoImage
        pil_img = Image.fromarray(resized_img)
        self.display_image = ImageTk.PhotoImage(pil_img)

        # Clear previous image
        self.canvas.delete("all")

        # Center image on canvas
        x = (canvas_w - new_w) // 2
        y = (canvas_h - new_h) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.display_image)

    def apply_grayscale(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first.")
            return

        # Convert to grayscale
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        # Convert grayscale to RGB for displaying correctly on canvas
        gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        self.show_image(gray_rgb)

if __name__ == "__main__":
    app = GrayscaleApp()
    app.root.mainloop()
