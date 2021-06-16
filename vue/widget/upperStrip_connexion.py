import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image


class UpperStrip(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # UPPER STRIP
        self._stripUpper = Canvas(self, height=75, highlightthickness=0)
        self._stripUpper.pack(fill=BOTH, expand=1)

        # LOGO
        self.logo = Image.open('images/logo.png')
        self.logo = self.logo.resize((150, 75), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo)

        # ID LOGO
        self.idPhoto = Image.open('images/id.png')
        self.idPhoto = self.idPhoto.resize([73, 73], Image.ANTIALIAS)
        self.idPhoto = ImageTk.PhotoImage(self.idPhoto)

        # SETTINGS AND ID BUTTON
        self.style = ttk.Style(self)
        self.style.configure("lefttab.TNotebook", tabposition="wn")

        self.mygrey = "#272727"
        self.mywhite = "white"

        self.style.theme_create("yummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": self.mygrey, "foreground": self.mywhite},
                "map": {"background": [("selected", self.mywhite)],
                        "foreground": [("selected", self.mygrey)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        self.style.theme_use("yummy")

        self.button = 0
        self.notebook = None

        self.idButton = Button(self, image=self.idPhoto, relief="flat", borderwidth=0, highlightthickness=0,
                               activebackground="#272727", bg="#272727")
        self.idButton.bind('<Button-1>', self._on_button_click)

        self._re_draw()
        self.bind("<Configure>", self._on_config)

    def _on_config(self, event):
        self._re_draw()

    def _re_draw(self):
        self._stripUpper.delete("all")
        # STRIP
        t = self.winfo_width()
        t = t - 75
        self._stripUpper.create_rectangle(0, 0, t, 75, outline='#272727', fill='#272727')
        self._stripUpper.create_image(0, 0, image=self.logo, anchor="nw")
        # ID NAME
        self._stripUpper.create_text(t - 100, 35, text='My game ID', fill='white', anchor="n")
        self.idButton.place(x=t, y=0)

    def _on_button_click(self, event):
        if self.button == 0:
            self.notebook = ttk.Notebook(None, style="lefttab.TNotebook")

            f1 = tk.Frame(self.notebook, bg=self.mygrey, width=300, height=400)
            f2 = tk.Frame(self.notebook, bg=self.mygrey, width=300, height=400)
            f3 = tk.Frame(self.notebook, bg=self.mygrey, width=300, height=400)

            text1 = Label(f1, text="On doit mettre quoi ici ?", bg=self.mygrey, fg=self.mywhite).pack()
            # text2 = Label(f2, text="Et là ?", bg=mygrey, fg=mywhite).pack()
            # text3 = Label(f3, text="Et ici ?", bg=mygrey, fg=mywhite).pack()

            # add what you want in each Frame

            self.notebook.add(f1, text="Mon Compte ")
            self.notebook.add(f2, text="Déconnexion")
            self.notebook.add(f3, text="Paramètres ")
            self.notebook.place(x=self.winfo_width() - 300, y=75, width=300, height=400)
            self.notebook.lift()
            self.button = 1
        else:
            self.notebook.destroy()
            self.button = 0


if __name__ == "__main__":
    root = tk.Tk()

    root.title("Games Folder")
    root.wm_attributes("-topmost", 1)

    strip = UpperStrip(root, bg="blue")
    strip.pack(expand=YES, fill="x", anchor="n")

    root.mainloop()
