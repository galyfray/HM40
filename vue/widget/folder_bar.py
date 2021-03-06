from tkinter import *


class FolderBar(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ___Button Favoris___
        button_fav = Button(self, text="Favoris", bg="#179EAF", fg="white", font=f"Times 12 bold")
        button_fav.grid(row=0, column=0, ipadx=40, ipady=10, sticky="nsew")
        # ___Button Tout___
        button_tout = Button(self, text="Tout", bg="#179EAF", fg="white", font=f"Times 12 bold")
        button_tout.grid(row=0, column=1, ipadx=40, ipady=10, sticky="nsew")
        # ___Button Aventure___
        button_aventure = Button(self, text="Aventure", bg="#179EAF", fg="white", font=f"Times 12 bold")
        button_aventure.grid(row=0, column=2, ipadx=40, ipady=10, sticky="nsew")
        # ___Button Solo___
        button_solo = Button(self, text="Solo", bg="#179EAF", fg="white", font=f"Times 12 bold")
        button_solo.grid(row=0, column=3, ipadx=40, ipady=10, sticky="nsew")
        # ___Button Action___
        button_action = Button(self, text="Action", bg="#179EAF", fg="white", font=f"Times 12 bold")
        button_action.grid(row=0, column=4, ipadx=40, ipady=10, sticky="nsew")

        for i in range(5):
            self.columnconfigure(i, weight=1)


if __name__ == "__main__":
    root = Tk()
    bar = FolderBar(root)
    bar.pack(expand=YES, fill=BOTH)
    root.mainloop()
    pass
