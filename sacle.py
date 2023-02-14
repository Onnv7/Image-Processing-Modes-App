import tkinter as tk

root = tk.Tk()
scale = tk.Scale(root, from_=0, to=100, orient="horizontal")
scale.pack()


def on_scale_change(val):
    value = int(val)
    print("The value of the scale is:", value)


scale.config(command=on_scale_change)

root.mainloop()
