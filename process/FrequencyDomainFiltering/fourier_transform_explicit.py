
import cv2
import numpy as np
import matplotlib.pyplot as plt


class FourierTransformExplicit:
    def __init__(self, image):
        self.image = image
        self.M = image.shape[0]
        self.N = image.shape[1]
        pass

    def convert_to_frequency_domain(self):
        f_xy = self.enlarge_photo()
        P, Q = 2*self.M, 2*self.N

        F_xy = np.zeros((P, Q))
        for x in range(P):
            for y in range(Q):
                F_xy[x, y] = f_xy[x, y] * np.power(-1, x + y)
        dft_col = dft_row = np.zeros((P, Q))

        for i in range(P):
            dft_col[i] = np.real(FourierTransformExplicit.DFT1D(F_xy[i]))
        # DFT chiều Q - theo hàng
        for j in range(Q):
            dft_row[:, j] = np.real(
                FourierTransformExplicit.DFT1D(dft_col[:, j]))
        print("Convert thanh cong")
        return dft_row

    def transform_into_the_spatial_domain(self, frequency_domain_image):
        f = np.asarray(self.image)

        P, Q = 2*self.M, 2*self.N

        idft_col = idft_row = np.zeros((P, Q))

        for i in range(P):
            idft_col[i] = FourierTransformExplicit.IDFT1D(
                frequency_domain_image[i])

        for j in range(Q):
            idft_row[:, j] = FourierTransformExplicit.IDFT1D(idft_col[:, j])
        g_array = np.asarray(idft_row.real)
        P, Q = np.shape(g_array)
        g_xy_p = np.zeros((P, Q))
        for x in range(P):
            for y in range(Q):
                g_xy_p[x, y] = g_array[x, y] * np.power(-1, x + y)
        return g_xy_p

    def get_mini_image(self, g_xy_p):
        g_xy = g_xy_p[:self.M, :self.N]
        return g_xy

    def enlarge_photo(self):
        f = np.asarray(self.image)
        P, Q = 2*self.M, 2*self.N
        # Chuyển ảnh PxQ vào mảng fp
        f_xy = np.zeros((P, Q))
        f_xy[:self.M, :self.N] = f
        f_xy = f_xy.astype(np.uint8)

        print("Enlarg thanh cong")
        return f_xy

    @staticmethod
    def DFT1D(img):
        U = len(img)
        outarry = np.zeros(U, dtype=complex)
        for m in range(U):
            sum = 0.0
            for n in range(U):
                e = np.exp(-1j * 2 * np.pi * m * n / U)
                sum += img[n] * e
            outarry[m] = sum
        return outarry

    @staticmethod
    def IDFT1D(img):
        U = len(img)
        outarry = np.zeros(U, dtype=complex)
        for n in range(U):
            sum = 0.0
            for m in range(U):
                e = np.exp(1j * 2 * np.pi * m * n / U)
                sum += img[m]*e
            pixel = sum/U
            outarry[n] = pixel
        return outarry
