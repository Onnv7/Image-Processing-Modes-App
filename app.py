import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox as msgbox
import cv2
import numpy as np
from adjust_frame import AdjustFrame
from function_frame import FunctionFrame
from mode_frame import ModeFrame
from controller import Controller
from view_frame import ViewFrame
from log_transformations import LogTransformations
from image_negatives import ImageNegative
from gamma import Gamma
from my_image import MyImage


class App(tk.Tk):
    my_image = MyImage()

    def __init__(self):
        super().__init__()
        self.controller = Controller(App.my_image)
        self.resizable(False, False)
        self.title("Form with Image Container")
        self.__create_widgets()

    def __create_widgets(self):
        view_frame = ViewFrame(self, self.controller)
        mode_frame = ModeFrame(self, self.controller)
        adjust_frame = AdjustFrame(self, self.controller)
        function_frame = FunctionFrame(self, self.controller)

        self.controller.set_frames(
            view_frame, mode_frame, adjust_frame, function_frame)

        view_frame.grid(
            row=0, column=1, sticky="nw", padx=50, pady=50)
        adjust_frame.grid(row=1, column=1, columnspan=2)
        mode_frame.grid(row=2, column=1, columnspan=2)
        function_frame.grid(
            row=3, column=1, columnspan=2, rowspan=2)

        for widget in function_frame.winfo_children():
            widget.grid_configure(padx=10, pady=50)


if __name__ == "__main__":
    app = App()
    app.mainloop()
