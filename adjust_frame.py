from tkinter import filedialog, ttk
import tkinter as tk

from log_transformations import LogTransformations


class AdjustFrame(tk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.c_slider = tk.Scale(self, from_=0, to=100,
                                 orient=tk.HORIZONTAL, sliderlength=20, width=20, length=200, troughcolor='blue', label="c")
        self.c_slider.config(command=self.controller.on_c_scale_change)

        self.gamma_slider = tk.Scale(self, from_=0, to=10,
                                     orient=tk.HORIZONTAL, sliderlength=20, width=20, length=200, resolution=0.1, troughcolor='red', label="gamma")
        self.gamma_slider.config(
            command=self.controller.on_gamma_scale_change)
