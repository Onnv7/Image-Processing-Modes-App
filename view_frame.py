
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import cv2


class ViewFrame(tk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.original_image_label = tk.Label(
            self, image=None, bg="blue", text="Original image")
        self.original_image_label.pack(side="left")

        self.result_image_label = tk.Label(
            self, image=None, bg="red", text="Resulting image")
        self.result_image_label.pack(side="left")
