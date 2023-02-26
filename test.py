import cv2
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
kernel = np.ones((3, 3), np.uint8)
img = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
min_img = cv2.erode(img, kernel)
print(min_img)
