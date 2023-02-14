import numpy as np


class Gamma:
    def __init__(self, image, c, gamma):
        self.my_image = image
        self.c = c
        self.gamma = gamma

    def process(self, gray_image):
        result = float(
            self.c) * pow(gray_image, float(self.gamma))
        self.my_image.result_image = np.round(result).astype(int)
