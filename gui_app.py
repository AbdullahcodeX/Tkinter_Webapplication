# from tkinter import *
# from PIL import Image, ImageTk
# ali_root = Tk()
#width x height
# ali_root.geometry("600x750")
# ali_root.minsize(200,100)
# abdullah =Label(text="my name is asa ds awan ")
# abdullah.pack()
# photo = PhotoImage(file="cat.jpg")
#for jpg image
# ali_root.minsize(500,300)
# image = Image.open("cat.jpg")
# photo = ImageTk.PhotoImage(image)
# awan_label = Label(image=photo)
# awan_label.pack()
# ali_root.mainloop()
import os
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk

# ----- CONFIGURE THIS PATH -----
IMAGE_FOLDER = r"D:\vs code\tkinter\images"  # <-- Change this to your image folder
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']

# ----- LOAD IMAGE FILES -----
image_files = [
    file for file in os.listdir(IMAGE_FOLDER)
    if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)
]

# Sort alphabetically (optional)
image_files.sort()

if not image_files:
    raise Exception("No image files found in the specified folder.")

# ----- MAIN WINDOW -----
root = Tk()
root.title("Image Viewer")
root.geometry("800x600")

# ----- FUNCTIONS -----
current_index = 0

def show_image(index):
    global img_label, image_display, title_label

    image_path = os.path.join(IMAGE_FOLDER, image_files[index])
    img = Image.open(image_path)
    img.thumbnail((700, 500))  # Resize if needed
    image_display = ImageTk.PhotoImage(img)

    img_label.config(image=image_display)
    img_label.image = image_display

    title_label.config(text=image_files[index])

    # Enable/disable buttons at ends
    prev_button.config(state="normal" if index > 0 else "disabled")
    next_button.config(state="normal" if index < len(image_files) - 1 else "disabled")


def next_image():
    global current_index
    if current_index < len(image_files) - 1:
        current_index += 1
        show_image(current_index)

def prev_image():
    global current_index
    if current_index > 0:
        current_index -= 1
        show_image(current_index)

# ----- WIDGETS -----
img_label = Label(root)
img_label.pack(pady=10)

title_label = Label(root, text="", font=("Arial", 14))
title_label.pack()

nav_frame = Frame(root)
nav_frame.pack(pady=20)

prev_button = Button(nav_frame, text="⬅ Previous", command=prev_image)
prev_button.grid(row=0, column=0, padx=10)

next_button = Button(nav_frame, text="Next ➡", command=next_image)
next_button.grid(row=0, column=1, padx=10)

# ----- INITIAL DISPLAY -----
show_image(current_index)

# ----- RUN -----
root.mainloop()

