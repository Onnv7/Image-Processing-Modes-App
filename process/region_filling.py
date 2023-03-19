import cv2
import numpy as np


class RegionFilling:
    DARK = 0
    WHITE = 1

    def __init__(self, image):
        self.my_image = image

    def process(self, location, color=0):
        height, width = self.my_image.image.shape[:2]
        threshval = 90
        n = 255
        img = self.my_image.image.copy()
        # retval, img = cv2.threshold(
        #     self.my_image.image, threshval, n, cv2.THRESH_BINARY)
        if int(color) == RegionFilling.WHITE:
            img = cv2.bitwise_not(img)
        kernel = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        X = np.zeros((height, width), np.uint8)
        X[location[0], location[1]] = 255
        kernel = np.asarray(kernel, np.uint8)
        Ac = img.copy()
        A = cv2.bitwise_not(Ac)
        while True:
            prev = X.copy()
            X = cv2.dilate(X, kernel, iterations=1)
            # print(prev.shape, X.shape)
            X = cv2.bitwise_and(X, Ac)
            if np.array_equal(prev, X):
                break
        filled = cv2.bitwise_or(A, X)
        if int(color) == RegionFilling.WHITE:
            filled = cv2.bitwise_not(filled)
        self.my_image.result_image = cv2.bitwise_not(filled)
