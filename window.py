import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
from log_transformations import LogTransformations
from my_image import MyImage

class Application:
    my_image = MyImage()
    
    def __init__(self, root, original_frame, original_image_label, result_frame, result_image_label, open_file_button):
        self.root = root
        self.original_frame = original_frame
        self.original_image_label = original_image_label
        self.result_frame = result_frame
        self.result_image_label = result_image_label
        self.open_file_button = open_file_button
    def create_app(self):
        self.open_file_button.config(command=Application.open_file)
        self.root.mainloop()
        
    @staticmethod
    def open_file():
        file_path = filedialog.askopenfilename()
        image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (500, 500))
        Application.my_image.image = image
        print(image.shape)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        original_image_label.config(image=image)
        original_image_label.image = image
        

root = tk.Tk()
root.title("Form with Image Container")
root.geometry('2000x1000+50+50')
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
open_file_button = tk.Button(root, text="Open Image")
open_file_button.grid(row=1, column=0)

app = Application(root, original_frame, original_image_label, result_frame, result_image_label, open_file_button)
app.create_app()