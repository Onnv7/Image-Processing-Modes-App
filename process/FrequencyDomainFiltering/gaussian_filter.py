
import math
import cv2
import numpy as np

from process.FrequencyDomainFiltering.fourier_transform import FourierTransform


class GaussianFilter():
    LOWPASS = 0
    HIGHPASS = 1

    def __init__(self, code, D0):
        # image = cv2.resize(src=image, dsize=(100, 100))
        # self.fourier_transform = None
        self.code = code
        self.D0 = D0

    def gaussian_filter(self, D0, height, width,):
        row_center = int(height/2)
        col_center = int(width/2)
        H = np.zeros((height, width))
        for u in range(height):
            for v in range(width):
                dist = math.sqrt(np.power(u-row_center, 2) +
                                 (np.power(v-col_center, 2)))
                H[u, v] = np.exp(-dist**2/(2*D0**2))
        if self.code == 0:
            print("Đang xử lý lowpass gaussian")
            return H
        elif self.code == 1:
            print("Đang xử lý highpass gaussian")
            return 1 - H

    def process_by_lib(self, img):
        height, width = img.shape
        img = cv2.resize(img, (100, 100))
        M, N = img.shape
        H = self.gaussian_filter(self.D0, M*2, N*2)

        obj = FourierTransform.DFT(img.copy())

        G = FourierTransform.apply_filter(obj, H)

        G = (G - G.min()) / (G.max() - G.min()) * 255
        G = G.astype('uint8')[:M, :N]
        g = cv2.resize(G, (height, width))
        return g
