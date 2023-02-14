import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox as msgbox
import cv2
import numpy as np
from log_transformations import LogTransformations
from image_negatives import ImageNegative
from gamma import Gamma
from my_image import MyImage


class Application:
    my_image = MyImage()
    root = tk.Tk()
    # frames
    old_mode = "None"
    image_frame = tk.Frame(root, bg="blue")
    adjust_frame = tk.Frame(root, bg="blue")
    mode_frame = tk.Frame(root, bg="blue")
    function_frame = tk.Frame(root, bg="blue", height=100)

    # labels
    original_image_label = tk.Label(
        image_frame, image=None, bg="blue")

    result_image_label = tk.Label(
        image_frame, image=None, bg="red")

    # combobox
    mode_combobox = ttk.Combobox(mode_frame, state="readonly")
    mode_combobox['values'] = ("None",
                               "Negative Image", "Log Transformations", "Gamma", 4, 5, "Text")
    mode_combobox.current(0)

    # buttons
    open_file_button = tk.Button(function_frame, text="Open Image")
    save_file_button = tk.Button(function_frame, text="Save Image")

    # scale
    c_slider = tk.Scale(adjust_frame, from_=0, to=100,
                        orient=tk.HORIZONTAL, sliderlength=20, width=20, length=200)

    gamma_slider = tk.Scale(adjust_frame, from_=0, to=10,
                            orient=tk.HORIZONTAL, sliderlength=20, width=20, length=200, resolution=0.1)

    def __init__(self):
        pass

    def create_app(self):
        Application.root.resizable(False, False)
        Application.root.title("Form with Image Container")
        # Application.root.geometry('2000x1000+50+50')

        # image frame
        Application.image_frame.grid(
            row=0, column=1, sticky="nw", padx=50, pady=50)

        # adjust frame
        Application.adjust_frame.grid(row=1, column=1, columnspan=2)

        # mode frame
        Application.mode_frame.grid(row=2, column=1, columnspan=2)

        # function frame
        Application.function_frame.grid(row=3, column=1, columnspan=2)
        for widget in Application.function_frame.winfo_children():
            widget.grid_configure(padx=10, pady=50)

        # image
        Application.original_image_label.pack(side="left")
        Application.result_image_label.pack(side="left")

        # mode combobox
        Application.mode_combobox.grid(column=0, row=0)
        Application.mode_combobox.bind(
            '<<ComboboxSelected>>', Application.selected_combobox)

        # button open file
        Application.open_file_button.grid(row=0, column=0)
        Application.open_file_button.config(command=Application.open_file)

        # button save file
        Application.save_file_button.grid(row=0, column=1)
        Application.save_file_button.config(
            command=Application.save_file)

        # slider
        Application.c_slider.config(command=Application.on_c_scale_change)
        Application.gamma_slider.config(
            command=Application.on_gamma_scale_change)
        Application.root.mainloop()

    @staticmethod
    def open_file():
        file_path = filedialog.askopenfilename()
        image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (500, 500))
        Application.my_image.image = image
        Application.my_image.result_image = image
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        Application.original_image_label.config(image=image)
        Application.original_image_label.image = image
        Application.selected_combobox(None)
        # Application.on_c_scale_change(Application.slider.get())

    @staticmethod
    def on_c_scale_change(c):
        if (Application.mode_combobox.get() == "Log Transformations"):
            log = LogTransformations(Application.my_image, c)
            log.process()
            Application.set_image_for_label(
                Application.my_image.result_image, Application.result_image_label, cv2.COLOR_BGR2RGB)
        else:
            Application.get_gamma_image()

    @staticmethod
    def on_gamma_scale_change(c):
        Application.get_gamma_image()

    @staticmethod
    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        cv2.imwrite(file_path, Application.my_image.result_image)

    @staticmethod
    def selected_combobox(e):
        Application.c_slider.grid_remove()
        Application.gamma_slider.grid_remove()
        if (Application.check_image() == False):
            msgbox.showinfo("Thông báo", "Hãy mở 1 file ảnh")
            print("Them ảnh vào")
            Application.mode_combobox.set(Application.old_mode)
            return

        if (Application.mode_combobox.get() == "None"):
            Application.my_image.result_image = Application.my_image.image.copy()
            return

        print("Bạn chọn...", Application.mode_combobox.get())
        Application.my_image.result_image = Application.my_image.image.copy()

        if (Application.mode_combobox.get() == "Negative Image"):
            Application.set_image_for_label(
                Application.my_image.image, Application.original_image_label)
            print("Thực hiện Image Negative")
            Application.get_image_negative()
        elif (Application.mode_combobox.get() == "Log Transformations"):
            Application.set_image_for_label(
                Application.my_image.image, Application.original_image_label)
            print("Thực hiện Log Transformations")
            Application.on_c_scale_change(Application.c_slider.get())
            Application.c_slider.grid(row=1, column=1)
        elif (Application.mode_combobox.get() == "Gamma"):
            print("Thực hiện Gamma")
            Application.c_slider.grid(row=1, column=1)
            Application.gamma_slider.grid(row=1, column=2)
            Application.get_gamma_image()

        print("BBBBBBBBB", Application.my_image.image.shape)
        Application.old_mode = Application.mode_combobox.get()

    @staticmethod
    def check_image():
        if not np.any(Application.my_image.image):
            return False
        return True

    @staticmethod
    def get_image_negative():
        image_negative = ImageNegative(Application.my_image)
        image_negative.process()
        Application.set_image_for_label(
            Application.my_image.result_image, Application.result_image_label, cv2.COLOR_BGR2RGB)

    # @staticmethod
    # def set_result_image():
    #     new_image = cv2.cvtColor(
    #         Application.my_image.result_image, cv2.COLOR_BGR2RGB)
    #     result = Image.fromarray(new_image)
    #     result = ImageTk.PhotoImage(result)
    #     Application.result_image_label.config(image=result)
    #     Application.result_image_label.image = result

    # @staticmethod
    # def get_gamma_image():
    #     image = cv2.cvtColor(Application.my_image.image, cv2.COLOR_RGB2GRAY)
    #     Application.my_image.result_image = image
    #     image = Image.fromarray(image)
    #     image = ImageTk.PhotoImage(image)
    #     Application.original_image_label.config(image=image)
    #     Application.original_image_label.image = image

    @staticmethod
    def set_RGB_image(matrix, label):
        image = cv2.cvtColor(matrix, cv2.COLOR_BGR2RGB)
        result = Image.fromarray(image)
        result = ImageTk.PhotoImage(result)
        label.config(image=result)
        label.image = result

    @staticmethod
    def set_image_for_label(matrix, label, code=None):
        image = None
        print(matrix)
        if code is None:
            # matrix = np.uint8(matrix)
            image = matrix
        else:
            image = cv2.cvtColor(matrix, code)
        result = Image.fromarray(image)
        result = ImageTk.PhotoImage(result)
        label.config(image=result)
        label.image = result

    @staticmethod
    def get_gamma_image():
        c = Application.c_slider.get()
        gamma = Application.gamma_slider.get()
        gray_image = cv2.cvtColor(
            Application.my_image.image, cv2.COLOR_BGR2GRAY)
        Application.set_image_for_label(
            gray_image, Application.original_image_label)

        gamma_image = Gamma(Application.my_image, c, gamma)
        gamma_image.process(gray_image)
        Application.set_image_for_label(
            Application.my_image.result_image, Application.result_image_label)
        print("AAAAAAAAAAAAAA", Application.my_image.image.shape)


app = Application()
app.create_app()
