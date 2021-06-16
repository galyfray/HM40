import json
from tkinter import *

from ViewInterface import Interface
from model.game import Game
from vue.widget.game_widget import GameGrid
from vue.widget.upperStrip_connexion import UpperStrip
from vue.widget.utils import ScrollableFrame

if __name__ == "__main__":
    root = Tk()

    root.title("Games Folder")
    root.wm_attributes("-topmost", 1)
    root.iconphoto(True, PhotoImage(file='images/iconTri.png'))

    interface = Interface(root, borderwidth=10, background="dark blue")
    interface.grid(row=0, column=0, sticky="NE")

    r_frame = Frame(bg="green")
    strip = UpperStrip(r_frame, bg="blue")
    strip.grid(row=0, column=0, stick="ew")
    r_frame.grid(row=0, column=1, sticky="nsew")

    sf = ScrollableFrame(r_frame)
    try:
        with open("config/games.json", "r") as f:
            gameList = json.load(f)
            print(gameList)
            gameList = [Game().deserialize(d) for d in gameList]
    except BaseException:
        gameList = [Game("Energie 4", ["python3", "Puissance 4/jeu.py"]),
                    Game("Serpent", ["python3", "Snake/snake.py"])]

    cr = GameGrid(sf, gameList)
    cr.grid(sticky="nsew")

    cr.sort_grid(lambda g: g.name, reverse=True)


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
    sf.grid(row=1, column=0, stick="nsew")

    r_frame.columnconfigure(0, weight=1)
    r_frame.rowconfigure(1, weight=1)

    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    root.geometry("900x600")


    def on_close():
        with open("config/games.json", "w+") as f:
            json.dump([g.serialize() for g in gameList], f, sort_keys=True, indent=4)
            f.close()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
