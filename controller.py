import math
import tkinter.messagebox as msgbox
from tkinter import filedialog
from PIL import Image, ImageTk

import cv2
import numpy as np
from process.FrequencyDomainFiltering.butterworth_filter import ButterworthFilter
from process.FrequencyDomainFiltering.gaussian_filter import GaussianFilter
from process.FrequencyDomainFiltering.ideal_filter import IdealFilter

from process.gamma import Gamma
from process.image_negatives import ImageNegative

from process.log_transformations import LogTransformations
from process.nonlinear_filter import NonlinearFilter


class Controller:
    old_mode = "None"

    def __init__(self, my_image):
        self.my_image = my_image

    def set_frames(self, view_frame, mode_frame, adjust_frame, function_frame, radio_frame):
        self.view_frame = view_frame
        self.mode_frame = mode_frame
        self.adjust_frame = adjust_frame
        self.function_frame = function_frame
        self.radio_frame = radio_frame

    # <<<<<<<<<<<<<<<<<<<< Utilities >>>>>>>>>>>>>>>>>>>
    def set_c_value_for_log_transformations(self, img):
        max_value = self.get_max_value(img)
        c_max = int(255 / math.log(max_value + 1))
        self.adjust_frame.c_slider.config(to=c_max)

    def get_max_value(self, image):
        arr = image.flatten()
        return np.amax(arr)

    def check_image(self):
        if self.my_image.image is None:
            return False
        return True

    def get_image_negative(self):
        image_negative = ImageNegative(self.my_image)
        image_negative.process()
        self.set_image_for_label(
            self.my_image.result_image.copy(), self.view_frame.result_image_label, "GRAY")

    def set_image_for_label(self, matrix, label, code="RGB"):
        image = matrix.copy()
        if code == "GRAY":
            image = matrix
        elif (code == "RGB"):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif (code == "GRAY2RGB"):
            image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)

        image = cv2.resize(image, (350, 350))
        result = Image.fromarray(image)
        result = ImageTk.PhotoImage(result)
        label.config(image=result)
        label.image = result
    # ======================================================================

    # <<<<<<<<<<<<<<<<<< Button's event >>>>>>>>>>>>>>>>>>>>>>
    def convert_from_BGR_to_GRAY(self):
        if (len(self.my_image.image.shape) == 3):
            self.my_image.result_image = self.my_image.image = cv2.cvtColor(
                self.my_image.image, cv2.COLOR_BGR2GRAY)
            self.set_image_for_label(
                self.my_image.image.copy(), self.view_frame.original_image_label, "GRAY")
            msgbox.showinfo(
                "Th??ng b??o", "???? chuy???n ?????i th??nh ???nh gray", icon="info")
            self.set_image_for_label(self.my_image.result_image.copy(
            ), self.view_frame.result_image_label, "GRAY")
        else:
            msgbox.showinfo("Th??ng b??o", "????y l?? ???nh Gray", icon="warning")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
        self.my_image.image = image.copy()
        self.my_image.result_image = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (350, 350))
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.view_frame.original_image_label.config(image=image)
        self.view_frame.original_image_label.image = image
        self.selected_combobox(None)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        cv2.imwrite(file_path, self.my_image.result_image)

    def apply_image(self):
        self.my_image.image = self.my_image.result_image.copy()
        if len(self.my_image.result_image.shape) == 3:
            self.set_image_for_label(
                self.my_image.image.copy(), self.view_frame.original_image_label, "RGB")
        elif (len(self.my_image.result_image.shape) == 2):
            self.set_image_for_label(
                self.my_image.image.copy(), self.view_frame.original_image_label, "GRAY")
        print("Applied")
        self.adjust_frame.c_slider.set(0)
        self.adjust_frame.gamma_slider.set(0)
        self.adjust_frame.kernel_size_slider.set(1)
        self.adjust_frame.D0_slider.set(1)
        self.adjust_frame.n_slider.set(1)
    # ======================================================================

    # <<<<<<<<<<<<<<<<<<<< scale's event >>>>>>>>>>>>>>>>>>
    def on_c_scale_change(self, c):
        if (self.mode_frame.mode_combobox.get() == "Log Transformations"):
            log = LogTransformations(self.my_image, c)
            log.process()
            self.set_image_for_label(
                self.my_image.result_image.copy(), self.view_frame.result_image_label, "RGB")
        else:
            self.get_gamma_image()

    def on_gamma_scale_change(self, c):
        self.get_gamma_image()

    def on_kernel_size_change(self, size):
        kernel_size = int(size) * 2 + 1
        self.adjust_frame.kernel_size_label.config(
            text="Kernel size: {}".format(kernel_size))
        filter = NonlinearFilter(self.my_image, kernel_size)
        if self.mode_frame.mode_combobox.get() == "Median Filter":
            filter.process(NonlinearFilter.MEDIAN)
        elif self.mode_frame.mode_combobox.get() == "Max Filter":
            filter.process(NonlinearFilter.MAX)
        elif self.mode_frame.mode_combobox.get() == "Min Filter":
            filter.process(NonlinearFilter.MIN)
        elif self.mode_frame.mode_combobox.get() == "MidPoint Filter":
            filter.process(NonlinearFilter.MID_POINT)
        self.set_image_for_label(self.my_image.result_image.copy(
        ), self.view_frame.result_image_label, "RGB")

    def get_gamma_image(self):
        c = self.adjust_frame.c_slider.get()
        gamma = self.adjust_frame.gamma_slider.get()
        original_image = self.my_image.image.copy()
        self.set_image_for_label(
            original_image, self.view_frame.original_image_label, "RGB")

        gamma_image = Gamma(self.my_image, c, gamma)
        gamma_image.process(original_image)
        self.set_image_for_label(
            self.my_image.result_image.copy(), self.view_frame.result_image_label, "RGB")

    def on_D0_change(self, c):
        self.radio_checked()
    # =============================================================
    # <<<<<<<<<<<<<<<<<<< radio's event >>>>>>>>>>>>>>>>>>>

    def radio_checked(self):
        self.adjust_frame.n_slider.grid_remove()
        D0 = self.adjust_frame.D0_slider.get()
        style = IdealFilter.LOWPASS
        if self.radio_frame.style.get() == "low":
            style = IdealFilter.LOWPASS
        elif self.radio_frame.style.get() == "high":
            style = IdealFilter.HIGHPASS

        if self.radio_frame.type.get() == "ideal":
            obj = IdealFilter(style, D0)
            self.my_image.result_image = obj.process_by_lib(
                self.my_image.image.copy())

        elif self.radio_frame.type.get() == "gaussian":
            obj = GaussianFilter(style, D0)
            self.my_image.result_image = obj.process_by_lib(
                self.my_image.image.copy())

        elif self.radio_frame.type.get() == "butterworth":
            self.adjust_frame.n_slider.grid(row=1, column=1)
            n = self.adjust_frame.n_slider.get()
            obj = ButterworthFilter(style, D0, n)
            self.my_image.result_image = obj.process_by_lib(
                self.my_image.image.copy())

        self.set_image_for_label(
            self.my_image.result_image.copy(), self.view_frame.result_image_label, "GRAY")

    # =============================================================

    # <<<<<<<<<<<<<<<<<<< combobox's event >>>>>>>>>>>>>>>>>>>

    def selected_combobox(self, e):
        self.adjust_frame.kernel_size_label.grid_remove()
        self.adjust_frame.c_slider.grid_remove()
        self.adjust_frame.gamma_slider.grid_remove()
        self.adjust_frame.kernel_size_slider.grid_remove()
        self.adjust_frame.D0_slider.grid_remove()
        self.adjust_frame.n_slider.grid_remove()
        self.radio_frame.style_filter_group.grid_remove()
        self.radio_frame.type_kernel_group.grid_remove()

        if (self.check_image() == False):
            msgbox.showinfo("Th??ng b??o", "H??y m??? 1 file ???nh")
            self.mode_frame.mode_combobox.set(Controller.old_mode)
            return

        if (self.mode_frame.mode_combobox.get() == "None"):
            self.my_image.result_image = self.my_image.image.copy()
            return

        your_choice = self.mode_frame.mode_combobox.get()
        print("B???n ch???n...", your_choice)
        self.set_image_for_label(self.my_image.image.copy(
        ), self.view_frame.original_image_label, "RGB")
        if (your_choice == "Negative Image"):
            print("Th???c hi???n Image Negative")
            self.get_image_negative()
        elif (your_choice == "Log Transformations"):
            self.set_c_value_for_log_transformations(
                self.my_image.image.copy())
            print("Th???c hi???n Log Transformations")
            self.on_c_scale_change(
                self.adjust_frame.c_slider.get())
            self.adjust_frame.c_slider.grid(row=1, column=1)
        # thao t??c tr??n gray image
        elif (your_choice == "Gamma"):
            print("Th???c hi???n Gamma")
            self.adjust_frame.c_slider.grid(row=1, column=1)
            self.adjust_frame.gamma_slider.grid(row=1, column=2)
            # Application.my_image.image = cv2.cvtColor(
            #     Application.my_image.image.copy(), cv2.COLOR_RGB2GRAY)
            self.get_gamma_image()
        elif your_choice == "Median Filter" or your_choice == "Max Filter" or your_choice == "Min Filter" or your_choice == "MidPoint Filter":
            if (len(self.my_image.image.shape) == 3):
                msgbox.showinfo(
                    "Warning", "Ch??? ????? n??y y??u c???u ???nh ph???i ??? d???ng gray. Vui l??ng chuy???n ?????i sang ???nh gray tr?????c khi s??? d???ng ch??? ????? n??y", icon="warning")
                self.mode_frame.mode_combobox.set("None")
                return
            print("Th???c hi???n filter")
            self.adjust_frame.kernel_size_slider.grid(row=1, column=1)
            self.adjust_frame.kernel_size_label.grid(row=0, column=1)
            self.on_kernel_size_change(
                self.adjust_frame.kernel_size_slider.get())

        elif your_choice == "Frequency domain filtering":
            print("nva", self.my_image.image.shape)
            if (len(self.my_image.image.shape) == 3):
                msgbox.showinfo(
                    "Warning", "Ch??? ????? n??y y??u c???u ???nh ph???i ??? d???ng gray. Vui l??ng chuy???n ?????i sang ???nh gray tr?????c khi s??? d???ng ch??? ????? n??y", icon="warning")
                self.mode_frame.mode_combobox.set("None")
                return
            print("Th???c hi???n l???c mi???n t???n s???")

            self.adjust_frame.D0_slider.grid(row=0, column=1)
            self.radio_frame.style_filter_group.grid(column=0, row=0)
            self.radio_frame.type_kernel_group.grid(
                column=1, row=0, sticky="w")
            self.radio_checked()
        Controller.old_mode = self.mode_frame.mode_combobox.get()
    # =================================================================
