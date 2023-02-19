
from tkinter import filedialog, ttk
import tkinter as tk
from PIL import Image, ImageTk
import cv2

from utilities import MyUtilities


class FunctionFrame(tk.Frame):

    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.configure(background="blue")
        self.open_file_button = tk.Button(self, text="Open Image")
        self.open_file_button.grid(row=0, column=0)
        self.open_file_button.config(command=self.controller.open_file)

        self.save_file_button = tk.Button(self, text="Save Image")
        self.save_file_button.grid(row=0, column=1)
        self.save_file_button.config(
            command=self.controller.save_file)

        self.apply_button = tk.Button(self, text="Apply")
        self.apply_button.grid(row=0, column=2)
        self.apply_button.config(
            command=self.controller.apply_image)

        self.gray_button = tk.Button(self, text="Convert to Gray Image")
        self.gray_button.grid(row=1, column=1)
        self.gray_button.config(
            command=self.controller.convert_from_BGR_to_GRAY)
