class ImageNegative:
    def __init__(self, image):
        self.my_image = image

    def process(self):
        self.my_image.result_image = 255 - self.my_image.image.copy()
