import tkinter as tk
from PIL import Image, ImageTk
class Interface():

    #fenêtre
    fen = tk.Tk()
    #Titre
    fen.title("Game Folder")
    #Geometry
    fen.geometry("900x600")
    #fen.iconbitmap("") #icon de fenêtre
    fen.config(background = "blue") #configuration
    #fen.resizable(width=True, height = True)#redimensionnement
    #____________Frame Menu_____________
    frame_menu = tk.Frame(fen, bd=10 )
    frame_menu.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="E")
    #___Image___
    image_logo = Image.open("logo.png")
    image_logo = image_logo.resize((160,140))
    img = ImageTk.PhotoImage(image_logo)
    logo = tk.Label(frame_menu,image=img)
    logo.grid(row=0, sticky=tk.W)
    #___Frame Label Trier par___
    Trier_par = tk.LabelFrame(frame_menu, text="Trier par")
    buttonRadio_Ordre_Alpha = tk.Radiobutton(Trier_par, text="Ordre Alphabétique")
    buttonRadio_Mes_Jeux = tk.Radiobutton(Trier_par, text="Mes jeux")
    buttonRadio_Plus_Recent = tk.Radiobutton(Trier_par, text="Plus récent")
    buttonRadio_Moins_joue = tk.Radiobutton(Trier_par, text="Moins joué")
    buttonRadio_Ordre_Alpha.grid(row=0, sticky=tk.W)
    buttonRadio_Mes_Jeux.grid(row=1,sticky=tk.W)
    buttonRadio_Plus_Recent.grid(row=2,sticky=tk.W)
    buttonRadio_Moins_joue.grid(row=3,sticky=tk.W)
    Trier_par.grid(row=1, sticky=tk.W)
    #___Button Fonctionnalitées___
    button_Jeu_aleatoire = tk.Button(frame_menu, text="Jeu aléatoire")
    button_Jeu_aleatoire.grid(row=2, sticky=tk.W)
    button_Autre_Fonction = tk.Button(frame_menu, text="Autre Fonctions...")
    button_Autre_Fonction.grid(row=3, sticky=tk.W)
    #____________Frame Générale_____________
    frame_generale = tk.Frame(fen)
    frame_generale.grid(row = 0, column=4, columnspan=6)

    #def __init__(self):

#main Pour tester l'interface
interface = Interface()
interface.fen.mainloop()