import cv2
import numpy as np
import scipy
from scipy.signal import medfilt2d
from scipy.ndimage import maximum_filter, minimum_filter


class NonlinearFilter():
    MIN = 0
    MEDIAN = 1
    MAX = 2
    MID_POINT = 3

    def __init__(self, image, kernel_size):
        self.my_image = image
        self.kernel_size = np.uint8(kernel_size)

    def process(self, mode):
        img = self.my_image.image
        if mode == NonlinearFilter.MEDIAN:
            # Viết tường minh
            self.my_image.result_image = NonlinearFilter.median_filter2(
                img, self.kernel_size)

            # Dùng thư viện
            # self.my_image.result_image = medfilt2d(
            #     img, kernel_size=self.kernel_size)
        elif mode == NonlinearFilter.MIN:

            # Viết tường minh
            self.my_image.result_image = NonlinearFilter.min_filter2(
                img, self.kernel_size)

            # Dùng thư viện
            # self.my_image.result_image = cv2.erode(img, np.ones(
            #     (self.kernel_size, self.kernel_size), np.uint8))
        elif mode == NonlinearFilter.MAX:

            # Viết tường minh
            self.my_image.result_image = NonlinearFilter.max_filter2(
                img, self.kernel_size)

            # Dùng thư viện
            # self.my_image.result_image = cv2.dilate(self.my_image.image, np.ones(
            #     (self.kernel_size, self.kernel_size), np.uint8))
        elif mode == NonlinearFilter.MID_POINT:
            # Viết tường minh
            self.my_image.result_image = NonlinearFilter.midpoint_filter2(
                img, self.kernel_size)
            # kernel = np.ones((self.kernel_size, self.kernel_size), np.uint8)
            # min_img = cv2.erode(img, kernel)
            # max_img = cv2.dilate(img, kernel)
            # midpoint = (min_img + max_img) / 2
            # self.my_image.result_image = midpoint.astype(np.uint8)

    @staticmethod
    def max_filter(image, kernel_size=3):
        filtered_img = maximum_filter(image, size=kernel_size)
        return filtered_img

    @staticmethod
    def min_filter(image, kernel_size=3):
        filtered_img = minimum_filter(image, size=kernel_size)
        return filtered_img

    @staticmethod
    def max_filter2(image, kernel_size=3):
        padding = kernel_size // 2

        padded_image = cv2.copyMakeBorder(
            image, padding, padding, padding, padding, cv2.BORDER_REFLECT)

        result = np.zeros_like(image)
        for i in range(padding, padded_image.shape[0] - padding):
            for j in range(padding, padded_image.shape[1] - padding):
                kernel = padded_image[i-padding:i +
                                      padding+1, j-padding:j+padding+1]
                max = np.amax(kernel)

                result[i-padding, j-padding] = max
        return result

    @staticmethod
    def min_filter2(image, kernel_size=3):
        padding = kernel_size // 2

        padded_image = cv2.copyMakeBorder(
            image, padding, padding, padding, padding, cv2.BORDER_REFLECT)

        result = np.zeros_like(image)
        for i in range(padding, padded_image.shape[0] - padding):
            for j in range(padding, padded_image.shape[1] - padding):
                kernel = padded_image[i-padding:i +
                                      padding+1, j-padding:j+padding+1]
                min = np.amin(kernel)

                result[i-padding, j-padding] = min
        return result

    @staticmethod
    def median_filter2(image, kernel_size=3):
        padding = kernel_size // 2

        padded_image = cv2.copyMakeBorder(
            image, padding, padding, padding, padding, cv2.BORDER_REFLECT)

        result = np.zeros_like(image)
        for i in range(padding, padded_image.shape[0] - padding):
            for j in range(padding, padded_image.shape[1] - padding):
                kernel = padded_image[i-padding:i +
                                      padding+1, j-padding:j+padding+1]
                median = np.median(kernel)

                result[i-padding, j-padding] = median
        return result

    @staticmethod
    def midpoint_filter2(image, kernel_size=3):
        padding = kernel_size // 2

        padded_image = cv2.copyMakeBorder(
            image, padding, padding, padding, padding, cv2.BORDER_REFLECT)

        result = np.zeros_like(image)
        for i in range(padding, padded_image.shape[0] - padding):
            for j in range(padding, padded_image.shape[1] - padding):
                kernel = padded_image[i-padding:i +
                                      padding+1, j-padding:j+padding+1]
                midpoint = (np.amax(kernel) + np.amin(kernel))/2

                result[i-padding, j-padding] = midpoint
        return result
