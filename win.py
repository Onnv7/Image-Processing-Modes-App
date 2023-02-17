import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

path = "./image/pic01.jpg"


image = cv2.imread(path)
cv2.imshow("image", image)
old = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
new = cv2.cvtColor(old, cv2.COLOR_GRAY2RGB)
print(image.shape, new.shape, old.shape)
cv2.imshow("NEW", new)

cv2.waitKey(10000000)
