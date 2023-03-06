from tkinter import filedialog, ttk
import tkinter as tk
import tkinter.messagebox as msgbox


class ModeFrame(tk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.mode_combobox = ttk.Combobox(self, state="readonly")
        self.mode_combobox['values'] = ("None",
                                        "Negative Image", "Log Transformations", "Gamma", "Median Filter", "Max Filter", "Min Filter", "MidPoint Filter", "Frequency domain filtering")
        self.mode_combobox.current(0)
        self.mode_combobox.grid(column=0, row=0)
        self.mode_combobox.bind(
            '<<ComboboxSelected>>', self.controller.selected_combobox)
