
import math
import cv2
import numpy as np


from process.FrequencyDomainFiltering.fourier_transform import FourierTransform

import matplotlib.pyplot as plt


class IdealFilter:
    LOWPASS = 0
    HIGHPASS = 1

    def __init__(self, code, D0):
        # image = cv2.resize(src=image, dsize=(100, 100))
        # self.fourier_transform = None
        self.code = code
        self.D0 = D0

    def ideal_filter(self, D0, height, width):
        row_center = int(height/2)
        col_center = int(width/2)
        H = np.zeros((height, width))
        if self.code == 0:
            print("Đang xử lý lowpass ideal")
            for u in range(height):
                for v in range(width):
                    dist = math.sqrt(np.power(u-row_center, 2) +
                                     (np.power(v-col_center, 2)))
                    if dist <= D0:
                        H[u, v] = 1
        elif self.code == 1:
            print("Đang xử lý highpass ideal")
            for u in range(height):
                for v in range(width):
                    dist = math.sqrt(np.power(u-row_center, 2) +
                                     (np.power(v-col_center, 2)))
                    if dist > D0:
                        H[u, v] = 1
        return H

    def process_by_lib(self, img):
        height, width = img.shape
        img = cv2.resize(img, (100, 100))
        M, N = img.shape
        H = None
        print("D0 = ", self.D0)
        H = self.ideal_filter(self.D0, M*2, N*2)

        obj = FourierTransform.DFT(img.copy())

        G = FourierTransform.apply_filter(obj, H)
        G = (G - G.min()) / (G.max() - G.min()) * 255
        G = G.astype('uint8')[:M, :N]
        # g = np.uint8(np.round(G))[:M, :N]
        g = cv2.resize(G, (height, width))
        return g
