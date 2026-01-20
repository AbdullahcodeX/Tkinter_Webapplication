import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from torchinfo import summary
import cv2
import numpy as np
import os
from ultralytics import YOLO  # Make sure ultralytics YOLO is installed

class ObjectDetectionGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YOLOv8 Object Detection")
        self.root.geometry("1000x700")

        # Variables
        self.current_image = None
        self.detections = []
        self.photo = None
        self.conf_threshold = 0.5

        # Load YOLO model
        self.model = YOLO('yolov8s.pt')

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        load_btn = ttk.Button(control_frame, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=(0, 10))

        detect_btn = ttk.Button(control_frame, text="Detect Objects", command=self.detect_objects)
        detect_btn.pack(side=tk.LEFT, padx=(0, 10))

        # New button to show model info in terminal
        info_btn = ttk.Button(control_frame, text="Show Model Info", command=self.show_model_info)
        info_btn.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(control_frame, text="Confidence:").pack(side=tk.LEFT, padx=(10, 5))
        self.conf_var = tk.DoubleVar(value=0.5)
        conf_scale = ttk.Scale(control_frame, from_=0.1, to=1.0, variable=self.conf_var, length=150)
        conf_scale.pack(side=tk.LEFT, padx=(0, 5))
        self.conf_label = ttk.Label(control_frame, text="0.5")
        self.conf_label.pack(side=tk.LEFT)
        conf_scale.configure(command=self.update_confidence)

        save_btn = ttk.Button(control_frame, text="Save Results", command=self.save_results)
        save_btn.pack(side=tk.RIGHT)

        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        self.canvas = tk.Canvas(image_frame, bg="white", width=600, height=450)
        self.canvas.pack()

        results_frame = ttk.LabelFrame(main_frame, text="Detection Results", padding="10")
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.results_listbox = tk.Listbox(results_frame, width=30, height=20)
        self.results_listbox.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(main_frame, text="Ready to load image ...")
        self.status_label.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            try:
                self.current_image = cv2.imread(file_path)
                self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
                self.detections = []
                self.display_image(self.current_image)
                self.update_results()
                self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")

    def display_image(self, image, draw_boxes=False):
        display_img = image.copy()

        if draw_boxes and self.detections:
            pil_img = Image.fromarray(display_img)
            draw = ImageDraw.Draw(pil_img)

            for det in self.detections:
                x1, y1, x2, y2 = det['bbox']
                draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
                label = f"{det['class']}: {det['confidence']:.2f}"
                draw.text((x1, y1 - 20), label, fill="red")

            display_img = np.array(pil_img)

        h, w = display_img.shape[:2]
        canvas_w, canvas_h = 600, 450
        scale = min(canvas_w / w, canvas_h / h)
        new_w, new_h = int(w * scale), int(h * scale)

        resized = cv2.resize(display_img, (new_w, new_h))
        pil_image = Image.fromarray(resized)
        self.photo = ImageTk.PhotoImage(pil_image)

        self.canvas.delete("all")
        x = (canvas_w - new_w) // 2
        y = (canvas_h - new_h) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)

    def detect_objects(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        try:
            temp_path = "temp_image.jpg"
            cv2.imwrite(temp_path, cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR))

            results = self.model(temp_path, conf=self.conf_var.get())

            self.detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for i in range(len(boxes)):
                        x1, y1, x2, y2 = boxes.xyxy[i].cpu().numpy()
                        confidence = boxes.conf[i].cpu().numpy()
                        class_id = int(boxes.cls[i].cpu().numpy())
                        class_name = self.model.names[class_id]

                        self.detections.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': confidence,
                            'class': class_name,
                            'class_id': class_id
                        })

            self.display_image(self.current_image, draw_boxes=True)
            self.update_results()
            self.status_label.config(text=f"Detected {len(self.detections)} objects")

            if os.path.exists(temp_path):
                os.remove(temp_path)

        except Exception as e:
            messagebox.showerror("Error", f"Detection failed: {str(e)}")

    def update_results(self):
        self.results_listbox.delete(0, tk.END)

        if not self.detections:
            self.results_listbox.insert(tk.END, "No objects detected")
            return

        for i, det in enumerate(self.detections):
            result_text = f"{i+1}. {det['class']} ({det['confidence']:.2f})"
            self.results_listbox.insert(tk.END, result_text)

    def update_confidence(self, value):
        self.conf_label.config(text=f"{float(value):.1f}")

    def save_results(self):
        if not self.detections:
            messagebox.showwarning("Warning", "No detections to save!")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )

        if save_path:
            try:
                result_img = self.current_image.copy()
                pil_img = Image.fromarray(result_img)
                draw = ImageDraw.Draw(pil_img)

                for det in self.detections:
                    x1, y1, x2, y2 = det['bbox']
                    draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                    label = f"{det['class']}: {det['confidence']:.2f}"
                    draw.text((x1, y1 - 25), label, fill="red")

                pil_img.save(save_path)
                self.status_label.config(text=f"Results saved to {os.path.basename(save_path)}")

            except Exception as e:
                messagebox.showerror("Error", f"Could not save results: {str(e)}")

    def show_model_info(self):
        try:
            # Print model summary to terminal
            info = summary(self.model.model, input_size=(1, 3, 640, 640), verbose=1)
            print(info)
        except Exception as e:
            print(f"Error printing model info: {e}")

    def run(self):
        self.root.mainloop()
    
print("\nYOLOv8 Object Detection implementation complete!")
print("Features available:")
print("- detect_objects(): Basic detection function")
print("- ObjectDetectionGUI: Complete tkinter application")

if __name__ == "__main__":
    app = ObjectDetectionGUI()
    app.run()
