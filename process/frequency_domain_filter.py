
import numpy as np


class FrequencyDomainFiltering:
    def __init__(self, style, type, image):
        self.my_image = image
        self.style = style
        self.type = type

    def process(self, original_image):
        result = float(
            self.c) * pow(original_image, float(self.gamma))
        self.my_image.result_image = np.array(
            np.round(result).astype(int), dtype="uint8")
