from tkinter import *


class FolderBar(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ___Button Favoris___
        button_fav = Button(self, text="Favoris")
        button_fav.grid(row=0, column=0)
        # ___Button Tout___
        button_tout = Button(self, text="Tout")
        button_tout.grid(row=0, column=1)
        # ___Button Aventure___
        button_aventure = Button(self, text="Aventure")
        button_aventure.grid(row=0, column=2)
        # ___Button Solo___
        button_solo = Button(self, text="Solo")
        button_solo.grid(row=0, column=3)
        # ___Button Action___
        button_action = Button(self, text="Action")
        button_action.grid(row=0, column=4)


if __name__ == "__main__":
    root = Tk()
    bar = FolderBar(root)
    bar.pack(expand=YES, fill=BOTH)
    root.mainloop()
    pass