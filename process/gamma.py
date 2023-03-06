import numpy as np


class Gamma:
    def __init__(self, image, c, gamma):
        self.my_image = image
        self.c = c
        self.gamma = gamma

    def process(self, original_image):
        result = float(
            self.c) * pow(original_image, float(self.gamma))
        self.my_image.result_image = np.array(
            np.round(result).astype(int), dtype="uint8")
