import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np

import matplotlib.pyplot as plt


def open_file():
    file_path = filedialog.askopenfilename()
    image = ImageTk.PhotoImage(file=file_path)
    image = cv2.resize(image, (500, 500))
    image_label.config(image=image)
    image_label.image = image


root = tk.Tk()
root.title("Form with Image Container")
root.geometry('1000x1000+50+50')


frame = tk.Frame(root, bg="white", width=500, height=500)
frame.pack(padx=50, pady=50)

image = cv2.imread("./image/pic03.PNG")

original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(original_image, (500, 500))
original_image = image
image = Image.fromarray(image)
image = ImageTk.PhotoImage(image)
# image = image.resize((300, 300), Image.ANTIALIAS)

image_label = tk.Label(frame, image=image)
image_label.pack(side="left", padx=20)


log_image_label = tk.Label(frame, image=image)
log_image_label.pack(side="left", padx=20)


def on_scale_change(c):
    img_bgr_clipped = np.maximum(original_image, original_image + 1)
    print("AN ", img_bgr_clipped)
    log_image = np.uint8(c)*(np.log(img_bgr_clipped))
    log_image = np.array(log_image, dtype='uint8')
    result = Image.fromarray(log_image)
    result = ImageTk.PhotoImage(result)
    log_image_label.config(image=result)
    log_image_label.image = result


open_file_button = tk.Button(frame, text="Open Image", command=open_file)
open_file_button.pack(side="bottom", pady=10)


slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, sliderlength=20,
                  width=20, length=200)
slider.pack()
slider.config(command=on_scale_change)


root.mainloop()
