# import bib
# import bib
import tkinter as tk

import Jeu

# création fenêtre
fen = tk.Tk()
# titre
fen.title("Démineur")
# taille
# fen.geometry("150x240")

frame_Top = tk.Frame(fen)
frame_Top.pack()
frame_general = tk.Frame(fen)
frame_general.pack()
frame_bottom = tk.Frame(fen)
frame_bottom.pack()
frame_result = tk.Frame(fen)
quitter = tk.Button(frame_bottom, text="Quitter", command=fen.destroy, relief=tk.GROOVE, bg="#179EAF")
quitter.grid(row=0, column=0)
label_titre_lose = tk.Label(frame_result, text="Perdu Dommage", height=2, relief=tk.GROOVE, fg='black',
                            font=("Calibri", 14), bg="#8b8b8b")
label_titre_win = tk.Label(frame_result, text="Félicitations Gagné !", height=2, relief=tk.SUNKEN, fg='black',
                           font=("Calibri", 12), bg="#8b8b8b")
game = 0
fen.resizable(width=False, height=False)


def NewGame(w, h, m):
    global game
    game = Jeu.Minefield(w, h, m)
    affichage()


def Reset():
    frame_bottom.pack_forget()
    frame_general.pack()
    frame_bottom.pack()
    frame_result.pack_forget()
    label_titre_win.pack_forget()
    label_titre_lose.pack_forget()
    # fen.geometry("150x240")
    NewGame(8, 8, 10)


reset = tk.Button(frame_bottom, text="Recommencer", command=Reset, relief=tk.GROOVE, bg="#179EAF")
reset.grid(row=0, column=1)


def hit(x, y):
    print("Hit:")
    print(str(x) + "/" + str(y))
    global game
    game.revelation(x, y)

    affichage()


def victory0rLose():
    i = 1
    print("Explosion" + str(game.get_explosions()))
    if game.get_explosions() != 0:
        # ajout texte
        frame_general.pack_forget()
        frame_bottom.pack_forget()
        label_titre_lose.pack()
        frame_result.pack()
        frame_bottom.pack()
        # fen.geometry("150x100")
        return 1
    if game.get_reaveled() == game.fieldMines and game.get_explosions() == 0:
        frame_general.pack_forget()
        frame_bottom.pack_forget()
        label_titre_win.pack()
        frame_result.pack()
        frame_bottom.pack()
        # fen.geometry("150x100")
        return 1


def affichage():
    global game
    if victory0rLose() != 0:
        game.toView(frame_general)
    # Boucle affichage
    fen.mainloop()
