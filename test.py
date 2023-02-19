import tkinter as tk


class FrameA(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.buttonA = tk.Button(
            self, text="Click me!", command=self.controller.update_text_b)
        self.textA = tk.Text(self)
        self.textA.insert(tk.END, "This is frame A")

        self.buttonA.pack()
        self.textA.pack()


class FrameB(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.buttonB = tk.Button(
            self, text="Click me!", command=self.controller.update_text_a)
        self.textB = tk.Text(self)
        self.textB.insert(tk.END, "This is frame B")

        self.buttonB.pack()
        self.textB.pack()


class Controller:
    def __init__(self):
        pass

    def set_frames(self, frame_a, frame_b):
        self.frame_a = frame_a
        self.frame_b = frame_b

    def update_text_a(self):
        print("btnB")
        text = self.frame_a.textA.get("1.0", tk.END)
        self.frame_a.textA.delete("1.0", tk.END)
        self.frame_a.textA.insert(tk.END, "111111")

    def update_text_b(self):
        print("btnA")
        text = self.frame_b.textB.get("1.0", tk.END)
        self.frame_b.textB.delete("1.0", tk.END)
        self.frame_b.textB.insert(tk.END, "222222")


class App:
    def __init__(self, master):
        self.master = master
        self.controller = Controller()

        self.frame_a = FrameA(self.master, self.controller)
        self.frame_b = FrameB(self.master, self.controller)

        self.controller.set_frames(self.frame_a, self.frame_b)

        self.frame_a.pack(side=tk.LEFT)
        self.frame_b.pack(side=tk.RIGHT)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
