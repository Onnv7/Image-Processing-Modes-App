from tkinter import *
from PIL import Image, ImageTk


class ImageEditor(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Load an image
        self.img = Image.open("./image/pic03.png")
        self.tkimg = ImageTk.PhotoImage(self.img)

        # Create a canvas and display the image
        self.canvas = Canvas(self, width=self.img.width,
                             height=self.img.height)
        self.canvas.create_image(0, 0, image=self.tkimg, anchor=NW)
        self.canvas.pack()

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.track_mouse)
        self.canvas.bind("<ButtonRelease-1>", self.stop_selection)

        # Initialize selection coordinates
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def start_selection(self, event):
        # Save the starting coordinates of the selection
        self.start_x = event.x
        self.start_y = event.y

        # Delete any existing selection rectangle
        self.canvas.delete("selection")

    def track_mouse(self, event):
        # Update the end coordinates of the selection
        self.end_x = event.x
        self.end_y = event.y

        # Delete any existing selection rectangle
        self.canvas.delete("selection")

        # Draw a new selection rectangle
        self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tags="selection"
        )

    def stop_selection(self, event):
        # Crop the selected area of the image
        box = (self.start_x, self.start_y, self.end_x, self.end_y)
        cropped_img = self.img.crop(box)

        # Display the cropped image
        cropped_tkimg = ImageTk.PhotoImage(cropped_img)
        self.canvas.create_image(
            self.img.width, 0, image=cropped_tkimg, anchor=NW)


root = Tk()
app = ImageEditor(master=root)
app.mainloop()
