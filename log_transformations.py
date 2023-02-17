from my_image import MyImage
import numpy as np
from PIL import Image, ImageTk


class LogTransformations():
    def __init__(self, image, c):
        self.c = c
        self.my_image = image

    def process(self):
        img_bgr_clipped = np.maximum(
            self.my_image.image.copy(), self.my_image.image.copy() + 1)
        log_image = np.uint8(self.c)*(np.log(img_bgr_clipped))
        print(log_image)
        self.my_image.result_image = np.array(log_image, dtype='uint8')
