from tkinter import *

from ViewInterface import Interface
from vue.widget.upperStrip_connexion import UpperStrip

if __name__ == "__main__":
    root = Tk()

    root.title("Games Folder")
    root.wm_attributes("-topmost", 1)

    interface = Interface(root, borderwidth=10, background="dark blue")
    interface.grid(row=0, column=0, sticky="NE")

    r_frame = Frame(bg="green")
    strip = UpperStrip(r_frame, bg="blue")
    strip.pack(expand=YES, fill="x", anchor="n")
    r_frame.grid(row=0, column=1, sticky="nsew")

    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    root.geometry("900x600")
    root.mainloop()
