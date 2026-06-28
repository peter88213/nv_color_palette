import tkinter as tk
from tkinter import ttk

from palettes import colorPalettes


class ColorPalette(ttk.Frame):

    def __init__(self, master, name, colors):
        super().__init__(master)
        ttk.Label(self, text=name).pack(fill='x', anchor='w')
        for i, c in enumerate(colors):
            ttk.Label(self, background=c, width=2).pack(side='left')


root = tk.Tk()

window = ttk.Frame(root)
window.pack(
    fill='both',
    padx=50,
    pady=5,
    anchor='w',
)
palettes = []
for p in colorPalettes:
    colorPalette = ColorPalette(window, p, colorPalettes[p])
    colorPalette.pack()
    palettes.append(colorPalette)

root.mainloop()

