from tkinter import filedialog, ttk
import tkinter as tk

from process.log_transformations import LogTransformations


class RadioFrame(tk.Frame):

    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.configure(background="#ffffff")

        # Tạo biến kiểm soát cho mỗi nhóm radio button
        self.style = tk.StringVar(value="low")
        self.type = tk.StringVar(value="ideal")

        # Nhóm 1
        self.style_filter_group = ttk.LabelFrame(self, text="Style filter")
        # self.style_filter_group.grid(column=0, row=0)

        self.lowpass_radio = tk.Radiobutton(
            self.style_filter_group, text="Lowpass", value="low", variable=self.style, command=self.controller.radio_checked)
        self.lowpass_radio.grid(column=0, row=0, sticky="w")

        self.hightpass_radio = tk.Radiobutton(
            self.style_filter_group, text="Hightpass", value="high", variable=self.style, command=self.controller.radio_checked)
        self.hightpass_radio.grid(column=0, row=1, sticky="w")

        # Nhóm 2
        self.type_kernel_group = ttk.LabelFrame(self, text="Type kernel")
        # self.type_kernel_group.grid(column=1, row=0)

        self.ideal_radio = tk.Radiobutton(
            self.type_kernel_group, text="Ideal", value="ideal", variable=self.type, command=self.controller.radio_checked)
        self.ideal_radio.grid(column=0, row=0, sticky="w")

        self.gaussian_radio = tk.Radiobutton(
            self.type_kernel_group, text="Gaussian", value="gaussian", variable=self.type, command=self.controller.radio_checked)
        self.gaussian_radio.grid(column=0, row=1, sticky="w")

        self.butterworth_radio = tk.Radiobutton(
            self.type_kernel_group, text="Butterworth", value="butterworth", variable=self.type, command=self.controller.radio_checked)
        self.butterworth_radio.grid(column=0, row=2, sticky="w")
