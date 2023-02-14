import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # self.pack()
        self.create_widgets()

    def create_widgets(self):

        original_frame = tk.Frame(root, bg="red", width=500, height=500)
        original_frame.grid(row=0, column=0, sticky="nw", padx=50, pady=50)

        result_frame = tk.Frame(root, bg="blue", width=500, height=500)
        result_frame.grid(row=0, column=1, sticky="nw", padx=50, pady=50)

    def open_image(self):
        # Mở file dialog để chọn file ảnh
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        # Nạp file ảnh vào frame trái
        if file_path:
            original_image = Image.open(file_path)
            image = ImageTk.PhotoImage(original_image)
            self.left_frame.image = image
            self.left_label = tk.Label(self.left_frame, image=image)
            self.left_label.pack(fill="both", expand=True)


root = tk.Tk()
root.title("Form with Image Container")
root.geometry('2000x1000+50+50')
app = Application(master=root)
app.mainloop()
