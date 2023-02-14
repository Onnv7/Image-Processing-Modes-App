class ImageNegative:
    def __init__(self, image):
        self.my_image = image

    def process(self):
        height, width = self.my_image.image.shape[:2]
        copy_image = self.my_image.image.copy()
        for i in range(0, height - 1):
            for j in range(0, width - 1):
                pixel = copy_image[i, j]
                pixel[0] = 255 - pixel[0]
                pixel[1] = 255 - pixel[1]
                pixel[2] = 255 - pixel[2]
                self.my_image.result_image[i, j] = pixel
