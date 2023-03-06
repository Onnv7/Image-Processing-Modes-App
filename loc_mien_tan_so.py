import math
import cv2
from matplotlib import pyplot as plt
import numpy as np

LOW = 0
HIGH = 1
D0 = 45
n = 2


def DFT1D(f):
    M = len(f)
    result_arr = np.zeros(M, dtype=complex)
    for u in range(M):
        F = 0.0
        for x in range(M):
            number = f[x]*np.exp(-1j*2*np.pi*u*x/M)
            F += number
        result_arr[u] = F
    return result_arr.real


def IDFT1D(F):
    M = len(F)
    result_arr = np.zeros(M, dtype=complex)
    for x in range(M):
        f = 0.0
        for u in range(M):
            number = F[u]*np.exp(1j*2*np.pi*u*x/M)
            f += number
        result_arr[x] = f/M
    return result_arr.real


def enlarge_image(image):
    h, w = image.shape[:2]
    new_image = np.zeros((h*2, w*2))
    new_image[:h, :w] = image
    return new_image


def shift(image):
    h, w = image.shape[:2]
    for i in range(h):
        for j in range(w):
            image[i, j] = image[i, j] * np.power(-1, i + j)

    return image


def ideal_filter(D0, height, width, code=0):
    row_center = int(height/2)
    col_center = int(width/2)
    H = np.zeros((height, width))
    if code == 0:
        for u in range(height):
            for v in range(width):
                dist = math.sqrt(np.power(u-row_center, 2) +
                                 (np.power(v-col_center, 2)))
                if dist <= D0:
                    H[u, v] = 1
    elif code == 1:
        for u in range(height):
            for v in range(width):
                dist = math.sqrt(np.power(u-row_center, 2) +
                                 (np.power(v-col_center, 2)))
                if dist > D0:
                    H[u, v] = 1
    return H


def butterworth_filter(D0, n, height, width, code=0):
    row_center = int(height/2)
    col_center = int(width/2)
    H = np.zeros((height, width))
    for u in range(height):
        for v in range(width):
            dist = math.sqrt(np.power(u-row_center, 2) +
                             (np.power(v-col_center, 2)))
            H[u, v] = 1/(1 + (dist/D0)**(2*n))
    if code == 0:
        return H
    elif code == 1:
        return 1 - H


def gaussian_filter(D0, height, width, code=1):
    row_center = int(height/2)
    col_center = int(width/2)
    H = np.zeros((height, width))
    for u in range(height):
        for v in range(width):
            dist = math.sqrt(np.power(u-row_center, 2) +
                             (np.power(v-col_center, 2)))
            H[u, v] = np.exp(-dist**2/(2*D0**2))
    if code == 0:
        return H
    elif code == 1:
        return 1 - H


if __name__ == "__main__":
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle(f"Lowpass Ideal: D0 = {D0}")
    # plt.title(f"Lowpass Gaussian: D0 = {D0}")
    # plt.title(f"Lowpass Butterworth: D0 = {D0}, n = {n}")

    # plt.title(f"Highpass Ideal: D0 = {D0}")
    # plt.title(f"Highpass Gaussian: D0 = {D0}")
    # plt.title(f"Highpass Butterworth: D0 = {D0}, n = {n}")
    image = cv2.imread("./image/pic12.jpg", cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (100, 100))

    # TIỀN XỬ LÝ
    original_image = np.asarray(image)
    enlarged_image = enlarge_image(original_image.copy())
    shifted_image1 = shift(enlarged_image.copy())
    height, width = shifted_image1.shape[:2]

    print(shifted_image1.shape)
    # CHUYỂN
    dft_row = dft_col = np.zeros((height, width))
    for i in range(height):
        dft_col[i] = DFT1D(shifted_image1[i])
    for i in range(width):
        dft_row[:, i] = DFT1D(dft_col[:, i])
    dft = dft_row.copy()

    # TODO:TÍNH
    H = gaussian_filter(D0, height, width, HIGH)
    G = np.multiply(dft, H)

    # CHUYỂN NGƯỢC
    idft_col = idft_row = np.zeros((height, width))
    for i in range(height):
        idft_col[i] = IDFT1D(G[i])
    for i in range(width):
        idft_row[:, i] = IDFT1D(idft_col[:, i])

    # RÚT KẾT QUẢ
    result_arr = idft_row.copy()

    shifted_image2 = shift(result_arr)
    result_image = shifted_image2[:int(height/2), :int(width/2)]

    # SHOW
    (ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9) = fig.subplots(3, 3)
    # Đọc và hiển thị ảnh gốc
    ax1.imshow(original_image, cmap='gray')
    ax1.set_title('Ảnh gốc MxN')
    ax1.axis('off')
    # Hiển thị ảnh mở rộng có kích thước PxQ
    ax2.imshow(enlarged_image, cmap='gray')
    ax2.set_title('Bước 1: Mở rộng ảnh')
    ax2.axis('off')
    # Hiển thị ảnh sau khi nhân -1 mũ (x+y)
    ax3.imshow(shifted_image1, cmap='gray')
    ax3.set_title('Bước 2: Xoay tâm')
    ax3.axis('off')
    # Hiển thị phổ tần số cảu anh sau khi biến đổi Fourier
    ax4.imshow(dft_row, cmap='gray')
    ax4.set_title('Bước 3: DFT')
    ax4.axis('off')
    # Hiển thị phổ tần số của bộ lọc
    ax5.imshow(H, cmap='gray')
    ax5.set_title(f'Bước 4: Bộ lọc H')
    ax5.axis('off')
    # Hiển thị phổ tần số của kết quả sau khi nhân Phổ tần số sau khi DFT
    # với bộ lọc
    ax6.imshow(G, cmap='gray')
    ax6.set_title('Bước 5: DFT * H')
    ax6.axis('off')
    # Hiển thị ảnh sau khi biến đổi ngược
    ax7.imshow(result_arr, cmap='gray')
    ax7.set_title('Bước 6.1: IDFT')
    ax7.axis('off')
    # Hiển thị phần thực của ảnh sau khi nhân -1 mũ (x+y)
    ax8.imshow(shifted_image2, cmap='gray')
    ax8.set_title('Bước 7: Xoay tâm')
    ax8.axis('off')
    # Hiển thị ảnh cuối cùng sau các bước, là ảnh cải thiện kích thước MxN
    ax9.imshow(result_image, cmap='gray')
    ax9.set_title('Bước 8: Kết quả')
    ax9.axis('off')

    plt.show()
