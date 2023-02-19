import tkinter.messagebox as msgbox
from tkinter import filedialog
from PIL import Image, ImageTk

import cv2
from gamma import Gamma
from image_negatives import ImageNegative

from log_transformations import LogTransformations


class Controller:
    old_mode = "None"

    def __init__(self, my_image):
        self.my_image = my_image

    def set_frames(self, view_frame, mode_frame, adjust_frame, function_frame):
        self.view_frame = view_frame
        self.mode_frame = mode_frame
        self.adjust_frame = adjust_frame
        self.function_frame = function_frame

    # <<<<<<<<<<<<<<<<<<<< Utilities >>>>>>>>>>>>>>>>>>>

    def check_image(self):
        if self.my_image.image is None:
            return False
        return True

    def get_image_negative(self):
        image_negative = ImageNegative(self.my_image)
        image_negative.process()
        self.set_image_for_label(
            self.my_image.result_image.copy(), self.view_frame.result_image_label, "RGB")

    def set_image_for_label(self, matrix, label, code="RGB"):
        image = matrix.copy()
        if code == "GRAY":
            image = matrix
        elif (code == "RGB"):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif (code == "GRAY2RGB"):
            image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)

        image = cv2.resize(image, (500, 500))
        result = Image.fromarray(image)
        result = ImageTk.PhotoImage(result)
        label.config(image=result)
        label.image = result
    # ======================================================================

    # <<<<<<<<<<<<<<<<<< Button's event >>>>>>>>>>>>>>>>>>>>>>
    def convert_from_BGR_to_GRAY(self):
        if (len(self.my_image.image.shape) == 3):
            self.my_image.image = cv2.cvtColor(
                self.my_image.image, cv2.COLOR_BGR2GRAY)
            self.set_image_for_label(
                self.my_image.image.copy(), self.view_frame.original_image_label, "GRAY")
        else:
            msgbox.showinfo("Thông báo", "Đây là ảnh Gray", icon="warning")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
        self.my_image.image = image.copy()
        self.my_image.result_image = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (500, 500))
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.view_frame.original_image_label.config(image=image)
        self.view_frame.original_image_label.image = image
        self.selected_combobox(None)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        cv2.imwrite(file_path, self.my_image.result_image)

    def apply_image(self):
        print("Applied")
        self.my_image.image = self.my_image.result_image.copy()
        if len(self.my_image.result_image.shape) == 3:
            self.set_image_for_label(
                self.my_image.image.copy(), self.view_frame.original_image_label, "RGB")
        elif (len(self.my_image.result_image.shape) == 2):
            self.set_image_for_label(
                self.my_image.image.copy(), self.view_frame.original_image_label, "GRAY")
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

    # =============================================================

    # <<<<<<<<<<<<<<<<<<< combobox's event >>>>>>>>>>>>>>>>>>>
    def selected_combobox(self, e):
        self.adjust_frame.c_slider.grid_remove()
        self.adjust_frame.gamma_slider.grid_remove()
        if (self.check_image() == False):
            msgbox.showinfo("Thông báo", "Hãy mở 1 file ảnh")
            self.mode_frame.mode_combobox.set(Controller.old_mode)
            return

        if (self.mode_frame.mode_combobox.get() == "None"):
            self.my_image.result_image = self.my_image.image.copy()
            return

        print("Bạn chọn...", self.mode_frame.mode_combobox.get())
        self.set_image_for_label(self.my_image.image.copy(
        ), self.view_frame.original_image_label, "RGB")
        if (self.mode_frame.mode_combobox.get() == "Negative Image"):
            print("Thực hiện Image Negative")
            self.get_image_negative()
        elif (self.mode_frame.mode_combobox.get() == "Log Transformations"):
            print("Thực hiện Log Transformations")
            self.on_c_scale_change(
                self.adjust_frame.c_slider.get())
            self.adjust_frame.c_slider.grid(row=1, column=1)
        # thao tác trên gray image
        elif (self.mode_frame.mode_combobox.get() == "Gamma"):
            print("Thực hiện Gamma")
            self.adjust_frame.c_slider.grid(row=1, column=1)
            self.adjust_frame.gamma_slider.grid(row=1, column=2)
            # Application.my_image.image = cv2.cvtColor(
            #     Application.my_image.image.copy(), cv2.COLOR_RGB2GRAY)
            self.get_gamma_image()
        Controller.old_mode = self.mode_frame.mode_combobox.get()
    # =================================================================
