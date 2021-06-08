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
    #fen.config(background = "blue") #configuration
    #fen.resizable(width=True, height = True)#redimensionnement
    #____________Frame Menu_____________
    frame_menu = tk.Frame(fen, borderwidth=10 )
    frame_menu.grid(row=0, column=0, sticky="E")
    #___Image___
    image_logo = Image.open("logo.png")
    image_logo = image_logo.resize((160,140))
    img = ImageTk.PhotoImage(image_logo)
    logo = tk.Label(frame_menu,image=img)
    #logo.grid(row=0, sticky=tk.W)
    logo.pack(fill=tk.BOTH,expand=tk.YES)
    #___Frame Label Trier par___
    Trier_par = tk.LabelFrame(frame_menu, text="Trier par")
    #___Buttons Radio___
    buttonRadio_Ordre_Alpha = tk.Radiobutton(Trier_par, text="Ordre Alphabétique")
    buttonRadio_Mes_Jeux = tk.Radiobutton(Trier_par, text="Mes jeux")
    buttonRadio_Plus_Recent = tk.Radiobutton(Trier_par, text="Plus récent")
    buttonRadio_Moins_joue = tk.Radiobutton(Trier_par, text="Moins joué")
    buttonRadio_Ordre_Alpha.grid(row=0, sticky=tk.W)
    buttonRadio_Mes_Jeux.grid(row=1,sticky=tk.W)
    buttonRadio_Plus_Recent.grid(row=2,sticky=tk.W)
    buttonRadio_Moins_joue.grid(row=3,sticky=tk.W)
    Trier_par.pack(fill=tk.BOTH,expand=tk.YES)
    #___Button Fonctionnalitées___
    button_Jeu_aleatoire = tk.Button(frame_menu, text="Jeu aléatoire")
    button_Jeu_aleatoire.pack(fill=tk.BOTH,expand=tk.YES)
    button_Autre_Fonction = tk.Button(frame_menu, text="Autre Fonctions...")
    button_Autre_Fonction.pack(fill=tk.BOTH,expand=tk.YES)
    #____________Frame Générale_____________
    frame_generale = tk.Frame(fen)
    frame_generale.grid(row = 0, column=1)
    #_______Frame Top_______
    frame_top = tk.Frame(frame_generale)
    frame_top.pack()
    # ___Image___
    image_logo2 = Image.open("logo.png")
    image_logo2 = image_logo2.resize((80, 70))
    img2 = ImageTk.PhotoImage(image_logo2)
    logo2 = tk.Label(frame_top, image=img2)
    logo2.grid(row=0,column=0,sticky=tk.W)
    #___Label UserName___
    label_username = tk.Label(frame_top, text="Username")
    label_username.grid(row=0,column=2,sticky=tk.E)
    #_______Frame Catégorie_______
    frame_categorie = tk.Frame(frame_generale)
    frame_categorie.pack()
    #___Button Favoris___
    button_fav = tk.Button(frame_categorie,text="Favoris")
    button_fav.grid(row=0, column=0)
    # ___Button Tout___
    button_tout = tk.Button(frame_categorie, text="Tout")
    button_tout.grid(row=0, column=1)
    # ___Button Aventure___
    button_aventure = tk.Button(frame_categorie, text="Aventure")
    button_aventure.grid(row=0, column=2)
    # ___Button Solo___
    button_solo = tk.Button(frame_categorie, text="Solo")
    button_solo.grid(row=0, column=3)
    # ___Button Action___
    button_action = tk.Button(frame_categorie, text="Action")
    button_action.grid(row=0, column=4)
    #______Frame Game_______
    frame_game = tk.Frame(frame_generale)
    frame_game.pack()
    #Ajouter la partie de Cyril


    #______Frame Bottom_______
    frame_bottom = tk.Frame(frame_generale)
    frame_bottom.pack()
    #___Label Crédits___
    label_credits = tk.Label(frame_bottom, text="Réaliser par Marie, Cyril, Romain, Baptiste dans le cadre de l'UV HM40")
    label_credits.pack(side=tk.BOTTOM)

    #def __init__(self):

#main Pour tester l'interface
interface = Interface()
interface.fen.mainloop()