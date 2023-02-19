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

# chỗ apply và chế độ gamma (1 kênh), viết code sao cho chỉ đổi mode mới cvt sang 3 kênh, còn apply thì vẫn giữ nguyên số kênh


class Application:
    my_image = MyImage()
    root = tk.Tk()
    # frames
    image_mode = "RGB"
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
    apply_button = tk.Button(function_frame, text="Apply")
    gray_button = tk.Button(function_frame, text="Convert to Gray Image")

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
        Application.function_frame.grid(
            row=3, column=1, columnspan=2, rowspan=2)
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

        # apply button
        Application.apply_button.grid(row=0, column=2)
        Application.apply_button.config(
            command=Application.apply_image)

        # convert button
        Application.gray_button.grid(row=1, column=1)
        Application.gray_button.config(
            command=Application.convert_from_BGR_to_GRAY)

        # slider
        Application.c_slider.config(command=Application.on_c_scale_change)
        Application.gamma_slider.config(
            command=Application.on_gamma_scale_change)
        Application.root.mainloop()
    # >>>>>>>>>>> Algorithm <<<<<<<<<<<<

    @staticmethod
    def get_image_negative():
        image_negative = ImageNegative(Application.my_image)
        image_negative.process()
        Application.set_image_for_label(
            Application.my_image.result_image.copy(), Application.result_image_label, "RGB")

    @staticmethod
    def get_gamma_image():
        # x = msgbox.showinfo(
        #     "Thông báo", "Sử dụng gamma sẽ đưa ảnh màu của bạn thành ảnh trắng đen", icon="warning", type="yesno")
        # print(x)
        c = Application.c_slider.get()
        gamma = Application.gamma_slider.get()
        original_image = Application.my_image.image.copy()
        Application.set_image_for_label(
            original_image, Application.original_image_label, "RGB")

        gamma_image = Gamma(Application.my_image, c, gamma)
        gamma_image.process(original_image)
        Application.set_image_for_label(
            Application.my_image.result_image.copy(), Application.result_image_label, "RGB")
    # =================================================================

    # >>>>>>>>>> utilities functions <<<<<<<<<

    @staticmethod
    def set_image_for_label(matrix, label, code="RGB"):
        image = matrix.copy()
        print("1: ", image.shape)
        if code == "GRAY":
            # matrix = np.uint8(matrix)
            print("KHONG DOI THANH RGB", code)
            image = matrix
        elif (code == "RGB"):
            print("DOI THANH RGB", code)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif (code == "GRAY2RGB"):
            print("GRAY2RGB")
            image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)

        print("2: ", image.shape)
        result = Image.fromarray(image)
        result = ImageTk.PhotoImage(result)
        label.config(image=result)
        label.image = result

    @staticmethod
    def check_image():
        if Application.my_image.image is None:
            return False
        return True

    @staticmethod
    def convert_from_BGR_to_GRAY():
        if (len(Application.my_image.image.shape) == 3):
            Application.my_image.image = cv2.cvtColor(
                Application.my_image.image, cv2.COLOR_BGR2GRAY)
            Application.set_image_for_label(
                Application.my_image.image.copy(), Application.original_image_label, "GRAY")
        else:
            msgbox.showinfo("Thông báo", "Đây là ảnh Gray", icon="warning")
    # ================================END=================================
    # >>>>>>>>>> function for button's click event <<<<<<<<<<<<<<<<<

    @ staticmethod
    def open_file():
        file_path = filedialog.askopenfilename()
        image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
        Application.my_image.image = image.copy()
        Application.my_image.result_image = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.resize(image, (500, 500))
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        Application.original_image_label.config(image=image)
        Application.original_image_label.image = image
        Application.selected_combobox(None)
        # Application.on_c_scale_change(Application.slider.get())

    @ staticmethod
    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        cv2.imwrite(file_path, Application.my_image.result_image)

    @ staticmethod
    def apply_image():
        print("Applied", Application.my_image.result_image.shape)
        Application.my_image.image = Application.my_image.result_image.copy()
        if len(Application.my_image.result_image.shape) == 3:
            # TODO: check color conversion
            Application.set_image_for_label(
                Application.my_image.image.copy(), Application.original_image_label, "RGB")
        elif (len(Application.my_image.result_image.shape) == 2):
            Application.set_image_for_label(
                Application.my_image.image.copy(), Application.original_image_label, "GRAY")
        # image = cv2.cvtColor(
        #     Application.my_image.image.copy(), cv2.COLOR_BGR2RGB)
        # image = Image.fromarray(image)
        # image = ImageTk.PhotoImage(image)
        # Application.original_image_label.config(image=image)
        # Application.original_image_label.image = image
    # =============== end ==============

    # >>>>>>>>>>>>> slider event <<<<<<<<<<

    @ staticmethod
    def on_c_scale_change(c):
        if (Application.mode_combobox.get() == "Log Transformations"):
            print("== == ==")
            log = LogTransformations(Application.my_image, c)
            log.process()
            Application.set_image_for_label(
                Application.my_image.result_image.copy(), Application.result_image_label, "RGB")
        else:
            Application.get_gamma_image()

    @ staticmethod
    def on_gamma_scale_change(c):
        Application.get_gamma_image()
    # ========================================

    # >>>>>>>>>>>>> combobox event <<<<<<<<<<
    @ staticmethod
    def selected_combobox(e):
        Application.c_slider.grid_remove()
        Application.gamma_slider.grid_remove()
        print(Application.my_image.image)
        if (Application.check_image() == False):
            msgbox.showinfo("Thông báo", "Hãy mở 1 file ảnh")
            print("Them ảnh vào")
            Application.mode_combobox.set(Application.old_mode)
            return

        if (Application.mode_combobox.get() == "None"):
            Application.my_image.result_image = Application.my_image.image.copy()
            return

        print("Bạn chọn...", Application.mode_combobox.get())
        # Application.my_image.result_image = Application.my_image.image.copy()
        # if (len(Application.my_image.image.shape) == 2):
        #     original_image = cv2.convertScaleAbs(
        #         Application.my_image.image.copy())
        #     result_image = cv2.convertScaleAbs(
        #         Application.my_image.result_image.copy())
        #     Application.my_image.image = cv2.cvtColor(
        #         original_image, cv2.COLOR_GRAY2BGR)
        #     Application.my_image.result_image = cv2.cvtColor(
        #         result_image, cv2.COLOR_GRAY2BGR)
        # mỗi lần đổi chế độ là phải đem ảnh lên màn trái
        Application.set_image_for_label(
            Application.my_image.image.copy(), Application.original_image_label, "RGB")
        if (Application.mode_combobox.get() == "Negative Image"):
            print("Thực hiện Image Negative")
            Application.get_image_negative()
        elif (Application.mode_combobox.get() == "Log Transformations"):
            print("Thực hiện Log Transformations")
            Application.on_c_scale_change(Application.c_slider.get())
            Application.c_slider.grid(row=1, column=1)
        # thao tác trên gray image
        elif (Application.mode_combobox.get() == "Gamma"):
            print("Thực hiện Gamma")
            # answer = "yes"
            # B, G, R = cv2.split(Application.my_image.image.copy())
            # print(B)
            # if np.array_equal(B, G):
            #     pass
            # else:
            #     answer = msgbox.showinfo(
            #         "Thông báo", "Nếu sử dụng chế độ này ảnh của bạn sẽ là ảnh trắng đen (ảnh xám) và không thể phục hồi lại ảnh màu. Bạn có muốn tiếp tục sử dụng chế độ này?", type="yesno")
            # if answer == "yes":
            Application.c_slider.grid(row=1, column=1)
            Application.gamma_slider.grid(row=1, column=2)
            # Application.my_image.image = cv2.cvtColor(
            #     Application.my_image.image.copy(), cv2.COLOR_RGB2GRAY)
            Application.get_gamma_image()
        Application.old_mode = Application.mode_combobox.get()
    # =================================================================


app = Application()
app.create_app()
