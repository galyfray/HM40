import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

root = tk.Tk()

root.title("Games Folder")
root.wm_attributes("-topmost", 1)

# UPPER STRIP
stripUpper = Canvas(root, width=root.winfo_screenwidth(), height=75, highlightthickness=0)
stripUpper.pack()

# STRIP
t = root.winfo_screenwidth()
print(t)
t = t - 75
stripUpper.create_rectangle(0, 0, t, 74, outline='#272727', fill='#272727')

# LOGO
logo = Image.open('logo.png')
logo = logo.resize((150, 75), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
stripUpper.create_image(0, 0, image=logo, anchor="nw")

# ID NAME
stripUpper.create_text(t - 100, 35, text='My game ID', fill='white', anchor="n")

# ID LOGO
idPhoto = Image.open('id.png')
idPhoto = idPhoto.resize([75, 75], Image.ANTIALIAS)
idPhoto = ImageTk.PhotoImage(idPhoto)

# SETTINGS AND ID BUTTON
style = ttk.Style(root)
style.configure("lefttab.TNotebook", tabposition="wn")

mygrey = "#272727"
mywhite = "white"

style.theme_create("yummy", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
    "TNotebook.Tab": {
        "configure": {"padding": [5, 1], "background": mygrey, "foreground": mywhite},
        "map": {"background": [("selected", mywhite)],
                "foreground": [("selected", mygrey)],
                "expand": [("selected", [1, 1, 1, 0])]}}})

style.theme_use("yummy")

button = 0
notebook = None


def settings(event):
    # TODO utiliser une classe pour stocker des infos dans self au lieux des var global
    global button
    global notebook
    if button == 0:
        notebook = ttk.Notebook(None, style="lefttab.TNotebook")

        f1 = tk.Frame(notebook, bg=mygrey, width=300, height=400)
        f2 = tk.Frame(notebook, bg=mygrey, width=300, height=400)
        f3 = tk.Frame(notebook, bg=mygrey, width=300, height=400)

        text1 = Label(f1, text="On doit mettre quoi ici ?", bg=mygrey, fg=mywhite).pack()
        # text2 = Label(f2, text="Et là ?", bg=mygrey, fg=mywhite).pack()
        # text3 = Label(f3, text="Et ici ?", bg=mygrey, fg=mywhite).pack()

        # add what you want in each Frame

        notebook.add(f1, text="Mon Compte ")
        notebook.add(f2, text="Déconnexion")
        notebook.add(f3, text="Paramètres ")
        notebook.place(x=root.winfo_screenwidth() - 300, y=75, width=300, height=400)
        notebook.lift()
        button = 1
    else:
        notebook.destroy()
        button = 0
    pass


idButton = Button(root, image=idPhoto, relief="flat", borderwidth=0, highlightthickness=0,
                  activebackground="#272727", bg="#272727")
idButton.bind('<Button-1>', settings)
idButton.place(x=t, y=0)

from game_widget import GameGrid
from utils import ScrollableFrame

g_frame = ScrollableFrame(root, bg="blue")

gd = GameGrid(g_frame)


def contconf(event):
    w = event.width // 5
    h = int(w / 0.65)
    for c in gd.containers:
        c.config(height=h)


g_frame.bind(
    "<Configure>",
    contconf,
    add="+"
)

g_frame.container.pack(fill=BOTH, expand=1, side=BOTTOM)
gd.grid(sticky="nsew")
g_frame.columnconfigure(0, weight=1)
g_frame.rowconfigure(0, weight=1)

root.mainloop()
