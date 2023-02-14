import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
from log_transformations import LogTransformations
from my_image import MyImage

my_image = MyImage(None, None)


def open_file():
    file_path = filedialog.askopenfilename()
    image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (500, 500))
    my_image.image = image
    print(image.shape)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    original_image_label.config(image=image)
    original_image_label.image = image


def log_transformation_process(image, result, c):
    machine = LogTransformations(image, result, c)
    return machine.process()


def on_scale_change(c):
    log_image = log_transformation_process(my_image.image, my_image.result_image, c)
    result = Image.fromarray(log_image)
    result = ImageTk.PhotoImage(result)
    result_image_label.config(image=result)
    result_image_label.image = result


root = tk.Tk()
root.title("Form with Image Container")
# root.geometry('2000x1000+50+50')

# original
original_frame = tk.Frame(root, bg="red", width=500, height=500)
original_frame.grid(row=0, column=0, sticky="nw", padx=50, pady=50)

original_image_label = tk.Label(original_frame, image=None)
original_image_label.pack(side="left", padx=0)


# result
result_frame = tk.Frame(root, bg="blue", width=500, height=500)
result_frame.grid(row=0, column=1, sticky="nw", padx=50, pady=50)

result_image_label = tk.Label(result_frame, image=None)
result_image_label.pack(side="left", padx=0)

# button open file
open_file_button = tk.Button(root, text="Open Image", command=open_file)
open_file_button.grid(row=1, column=0)


# button save image
# def save_file(image):
#     file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
#     cv2.imwrite(file_path, image)


# save_button = tk.Button(root, text="Save File",
#                         command=save_file(my_image.result_image))
# save_button.pack()

# bar
slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                  sliderlength=20, width=20, length=200)
slider.grid(row=1, column=1)
slider.config(command=on_scale_change)

# radio button

var = tk.IntVar()


def selection():
    selection = "You selected " + str(var.get())
    print(selection)


radio_frame = tk.Frame(root)
radio_frame.grid(row=2, column=1, columnspan=2, sticky="nsew")


radio_button_1 = tk.Radiobutton(
    radio_frame, text="Option 1", variable=var, value=1, command=selection)
radio_button_1.pack(anchor=tk.W)

radio_button_2 = tk.Radiobutton(
    radio_frame, text="Option 2", variable=var, value=2, command=selection)
radio_button_2.pack(anchor=tk.W)

root.mainloop()
