import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# ----- SETUP -----
root = Tk()
root.title("Tkinter Web-Style App")
root.geometry("900x600")

# ----- NAVBAR -----
navbar = Frame(root, bg="#1f1f1f", height=50)
navbar.pack(fill=X)

home_btn = Button(navbar, text="Home", bg="#1f1f1f", fg="white", bd=0, padx=20)
home_btn.pack(side=LEFT, padx=10)

upload_btn_nav = Button(navbar, text="Upload", bg="#1f1f1f", fg="white", bd=0, padx=20)
upload_btn_nav.pack(side=LEFT)

# ----- MAIN CONTENT -----
content_frame = Frame(root)
content_frame.pack(fill=BOTH, expand=True)

# Load background image
bg_image_path = "D:\vs code\tkinter\images\cat (2).jpg"  # <- Replace with your background image path
if not os.path.exists(bg_image_path):
    print("Warning: Background image not found!")

# Function to place background
def set_background():
    try:
        bg_img = Image.open(bg_image_path)
        bg_img = bg_img.resize((900, 550))
        bg_img_tk = ImageTk.PhotoImage(bg_img)

        bg_label = Label(content_frame, image=bg_img_tk)
        bg_label.image = bg_img_tk  # prevent garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        content_frame.config(bg="#cccccc")

set_background()

# ----- TEXT OVER BACKGROUND -----
text_label = Label(content_frame,
                   text="Welcome to the Image Uploader!",
                   font=("Helvetica", 24, "bold"),
                   bg="white",
                   fg="black")
text_label.place(relx=0.5, rely=0.3, anchor="center")

# Uploaded image label
uploaded_img_label = Label(content_frame, bg="white")
uploaded_img_label.place(relx=0.5, rely=0.65, anchor="center")

# ----- FUNCTION TO UPLOAD IMAGE -----
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        uploaded_img_label.config(image=img_tk)
        uploaded_img_label.image = img_tk

# ----- UPLOAD BUTTON -----
upload_button = Button(content_frame,
                       text="Upload Image",
                       command=upload_image,
                       bg="#4CAF50",
                       fg="white",
                       padx=20,
                       pady=10,
                       font=("Arial", 12, "bold"))
upload_button.place(relx=0.5, rely=0.5, anchor="center")

# ----- MAINLOOP -----
root.mainloop()
