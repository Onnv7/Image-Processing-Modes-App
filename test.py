import numpy as np
import cv2
from matplotlib import pyplot as plt

# đọc ảnh đầu vào
img = cv2.imread('./image/pic12.jpg', 0)

# tính FFT và dịch chuyển tâm ảnh về giữa
F = np.fft.fftshift(np.fft.fft2(img))

# áp dụng bộ lọc trên phổ tần số

# dịch chuyển tâm về vị trí ban đầu
F = np.fft.ifftshift(F)

# tính ngược FFT để có ảnh mới
img_new = np.abs(np.fft.ifft2(F))

# hiển thị ảnh
plt.imshow(img_new, cmap='gray')
plt.show()
