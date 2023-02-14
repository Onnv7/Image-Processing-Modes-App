import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
from log_transformations import LogTransformations
from my_image import MyImage

class Application:
    my_image = MyImage()
    root = tk.Tk()
    result_frame = tk.Frame(root, bg="blue", width=500, height=500)
    result_image_label = tk.Label(result_frame, image=None)
    open_file_button = tk.Button(root, text="Open Image")
    original_frame = tk.Frame(root, bg="red", width=500, height=500)
    original_image_label = tk.Label(original_frame, image=None)
    slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                  sliderlength=20, width=20, length=200)
    def __init__(self):
        pass
    def create_app(self):
        Application.root.title("Form with Image Container")
        Application.root.geometry('2000x1000+50+50')
        Application.original_frame.grid(row=0, column=0, sticky="nw", padx=50, pady=50)

        Application.original_image_label.pack(side="left", padx=0)

        # result
        Application.result_frame.grid(row=0, column=1, sticky="nw", padx=50, pady=50)

        Application.result_image_label.pack(side="left", padx=0)

        # button open file
        Application.open_file_button.grid(row=1, column=0)  
        Application.open_file_button.config(command=Application.open_file)
        
        # slider
        Application.slider.grid(row=1, column=1)
        Application.slider.config(command=Application.on_scale_change)
        
        
        Application.root.mainloop()    
    @staticmethod
    def open_file():
        file_path = filedialog.askopenfilename()
        image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (500, 500))
        Application.my_image.image = image
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        Application.original_image_label.config(image=image)
        Application.original_image_label.image = image
    
    @staticmethod
    def on_scale_change(c):
        print(Application.my_image.image)
        machine = LogTransformations(Application.my_image, c)
        machine.process()
        result = Image.fromarray(Application.my_image.result_image)
        result = ImageTk.PhotoImage(result)
        Application.result_image_label.config(image=result)
        Application.result_image_label.image = result 




app = Application()
app.create_app()