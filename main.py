import os
from tkinter import *

from PIL import Image

from model.game import GameList, Game
from vue.ViewInterface import Interface
from vue.widget.folder_bar import FolderBar
from vue.widget.game_widget import GameGrid
from vue.widget.upperStrip_connexion import UpperStrip
from vue.widget.utils import ScrollableFrame

if __name__ == "__main__":
    root = Tk()

    root.title("Games Folder")
    root.wm_attributes("-topmost", 1)
    root.iconphoto(True, PhotoImage(file='images/iconTri.png'))

    interface = Interface(root, borderwidth=10, background="#272727")
    interface.grid(row=0, column=0, sticky="NE")

    r_frame = Frame(bg="green")
    r_frame.grid(row=0, column=1, sticky="nsew")

    strip = UpperStrip(r_frame, bg="blue")
    strip.grid(row=0, column=0, stick="ew")

    folders = FolderBar(r_frame)
    folders.grid(row=1, column=0, stick="ew")

    sf = ScrollableFrame(r_frame, background="#474747")
    sf.grid(row=2, column=0, stick="nsew")

    gameList = GameList()
    gameList.load_from_file()

    for subdir, dirs, files in os.walk("./images/fakeGames"):
        for file in files:
            filepath = subdir + os.sep + file
            gameList.add_game(Game(file[:file.rfind(".")], "", Image.open(filepath), ))

    cr = GameGrid(sf, gameList)
    cr.grid(sticky="nsew")

    gameList.set_reverse(False)


    def contconf(event):
        col = event.width // 150
        if col != cr.get_nb_col():
            cr.set_nb_col(col)
        w = event.width // cr.get_nb_col()
        h = int(w / cr.get_ratio())
        for c in cr.containers:
            c.config(height=h)


    sf.bind(
        "<Configure>",
        contconf,
        add="+"
    )

    sf.columnconfigure(0, weight=1)

    r_frame.columnconfigure(0, weight=1)
    r_frame.rowconfigure(2, weight=1)

    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    root.geometry("900x600")


    def on_close():
        gameList.dump_to_file()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
