from tkinter import *

from vue.widget.upperStrip_connexion import UpperStrip

if __name__ == "__main__":
    root = Tk()

    root.title("Games Folder")
    root.wm_attributes("-topmost", 1)

    strip = UpperStrip(root, bg="blue")
    strip.pack(expand=YES, fill="x", anchor="n")

    root.mainloop()
