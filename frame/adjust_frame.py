from tkinter import filedialog, ttk
import tkinter as tk

from process.log_transformations import LogTransformations


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

        self.kernel_size_slider = tk.Scale(self, from_=1, to=49, orient=tk.HORIZONTAL, sliderlength=20,
                                           width=20, length=200, showvalue=0,                                  troughcolor='green', label="Kernel size", resolution=1)
        self.kernel_size_label = tk.Label(self, text="")

        self.kernel_size_slider.config(
            command=self.controller.on_kernel_size_change)

        self.D0_slider = tk.Scale(self, from_=1, to=400,
                                  orient=tk.HORIZONTAL, sliderlength=20, width=20, length=300, resolution=1, troughcolor='red', label="D0")
        self.D0_slider.config(
            command=self.controller.on_D0_change)

        self.n_slider = tk.Scale(self, from_=1, to=50,
                                 orient=tk.HORIZONTAL, sliderlength=20, width=20, length=150, resolution=0.1, troughcolor='red', label="D0")
        self.n_slider.config(
            command=self.controller.on_D0_change)
