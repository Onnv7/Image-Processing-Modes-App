import cv2
import numpy as np
from matplotlib import pyplot as plt


class FourierTransform:
    def __init__(self):
        pass

    @staticmethod
    def DFT(img):
        # Mở rộng ảnh

        height, width = img.shape[:2]
        new_height, new_width = height*2, width*2

        # Tạo ảnh mới
        new_img = np.zeros((new_height, new_width))

        # Đặt ảnh gốc vào ảnh mới
        new_img[0:height, 0:width] = img
        F = np.fft.fft2(new_img)
        return np.fft.fftshift(F)

    @staticmethod
    def apply_filter(F, H):
        G = F * H
        g = np.fft.ifft2(np.fft.ifftshift(G))
        g = np.real(g)
        return g

    # @staticmethod
    # def DFT(img):
    #     # Mở rộng ảnh

    #     height, width = img.shape[:2]
    #     new_height, new_width = height*2, width*2

    #     # Tạo ảnh mới
    #     new_img = np.zeros((new_height, new_width), np.uint8)

    #     # Đặt ảnh gốc vào ảnh mới
    #     new_img[0:height, 0:width] = img
    #     new_img = np.fft.fftshift(new_img)
    #     F = np.fft.fft2(new_img)
    #     return F

    # @staticmethod
    # def apply_filter(F, H):
    #     G = F * H
    #     g = np.fft.ifft2(G)
    #     g = np.real(g)
    #     return np.fft.ifftshift(g)
