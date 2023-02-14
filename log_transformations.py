from my_image import MyImage
import numpy as np
from PIL import Image, ImageTk


class LogTransformations(MyImage):
    def __init__(self, image, result_image, c):
        MyImage.__init__(self, image, result_image)
        self.c = c

    def process(self):
        img_bgr_clipped = np.maximum(self.image, self.image + 1)
        log_image = np.uint8(self.c)*(np.log(img_bgr_clipped))
        log_image = np.array(log_image, dtype='uint8')
        return log_image
