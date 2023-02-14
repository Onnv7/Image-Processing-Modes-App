import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
    cv2.imwrite(file_path, image)


root = tk.Tk()
root.title("Save Image")

save_button = tk.Button(root, text="Save File", command=save_file)
save_button.pack()

root.mainloop()
