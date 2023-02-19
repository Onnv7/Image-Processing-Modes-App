import cv2
from gamma import Gamma
from my_image import MyImage
from PIL import Image, ImageTk


class MyUtilities:
    def __init__(self, app, view_frame, mode_frame, adjust_frame, function_frame):
        self.my_image = MyImage()
        self.app = app
        self.view_frame = view_frame
        self.mode_frame = mode_frame
        self.adjust_frame = adjust_frame
        self.function_frame = function_frame
        pass

    def get_gamma_image(self):
        c = self.adjust_frame.c_slider.get()
        gamma = self.adjust_frame.gamma_slider.get()
        original_image = self.my_image.image.copy()
        self.view_frame.set_image_for_label(
            original_image, self.view_frame.original_image_label, "RGB")

        gamma_image = Gamma(self.my_image, c, gamma)
        gamma_image.process(original_image)
        self.set_image_for_label(
            self.my_image.result_image.copy(), self.view_frame.result_image_label, "RGB")

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
