from random import *
from copy import *
from tkinter import *
import time
import tkinter as tk

fen1 = Tk()


def grille ():

    grille = [] #création de la liste finale
    
    for j in range (0,6) :
        ligne = [] #liste stockant les lignes
        for i in range (0,7) :
            case="-"
            ligne.append(case)#concatenation de colonnes 
        grille.append(ligne)#ajout de la ligne à la grille

    return grille


def afficher(grille):

    #point initial (250,100)
    x_init = 250
    y_init = 100
    e = 3 #épaisseur pion
    
    xn = x_init 
    yn = y_init
    xm = x_init + 40
    ym = y_init + 40
    
    for li in range (0,6):
        for co in range (0,7):
            
            carre = dessin.create_rectangle(xn, yn, xm, ym, width=2, outline='darkblue', fill='darkblue')
            
            if grille [li][co]=="O":
                cercleJ = dessin.create_oval(xn+e, yn+e, xm-e, ym-e, width=2, outline='yellow', fill='yellow')
                
            elif grille[li][co]=="X":
                cercleR = dessin.create_oval(xn+e, yn+e, xm-e, ym-e, width=2, outline='red', fill='red')
 
            else :
                cercleV = dessin.create_oval(xn+e, yn+e, xm-e, ym-e, width=2, outline='dimgrey', fill='dimgrey')

            xn = xn + 40
            yn = yn
            xm = xm + 40
            ym = ym
            
        xn = x_init
        yn = yn + 40
        xm = x_init + 40
        ym = ym + 40
            
    dessin.update()
    
    return


def joueur ():

    j=randint(1,2) #choix du joueur qui débute (aléatoire)
    
    if (j == 1):
        J1=1 #lorsque le tour est impair, le joueur 1 joue
        #texte = dessin.create_text(380, 450, fill="red", text="Joueur 1 commence la partie", font=("Helvetica",20))
        J2=2 #lorsque le tour est pair, le joueur 2 joue 
    else :
        J1=2 #lorsque le tour est pair, le joueur 1 joue
        #texte = dessin.create_text(380, 450, fill="yellow", text="Joueur 2 commence la partie", font=("Helvetica",20))
        J2=1 #lorsque le tour est impair, le joueur 2 joue

    print ("J1 = ", J1)
    print ("J2 = ", J2)
    print()

    dessin.update()
   
    return [J1, J2]

def clickPion():

    dessin.bind('<Button-1>', positionPion)

    return


def positionPion(event):

    #Si nous sommes bien dans la grille de jeu ...
    if 250 < event.x < 530 and 100 < event.y < 340 :

        # Zone clickable : colonne 1
        if 250 < event.x < 290 :
            if grille[0][0] == '-' : # et s'il reste au moins une place dans la colonne ...
                ajouterPion(0)
            else :
                erreur_jeu(1)

        # Zone clickable : colonne 2
        elif 290 < event.x < 330 :
            if grille[0][1] == '-' :
                ajouterPion(1)
            else :
                erreur_jeu(2)
            
        # Zone clickable : colonne 3
        elif 330 < event.x < 370 :
            if grille[0][2] == '-' :
                ajouterPion(2)
            else :
                erreur_jeu(3)
            
        # Zone clickable : colonne 4
        elif 370 < event.x < 410 :
            if grille[0][3] == '-' :
                ajouterPion(3)
            else :
                erreur_jeu(4)
            
        # Zone clickable : colonne 5
        elif 410 < event.x < 450 :
            if grille[0][4] == '-' :
                ajouterPion(4)
            else :
                erreur_jeu(5)
            
        # Zone clickable : colonne 6
        elif 450 < event.x < 490 :
            if grille[0][5] == '-' :
                ajouterPion(5)
            else :
                erreur_jeu(6)
            
        # Zone clickable : colonne 7
        elif 490 < event.x < 530 :
            if grille[0][6] == '-' :
                ajouterPion(6)
            else :
                erreur_jeu(7)
        
    return

def erreur_jeu():       #Fonction qui s'affiche pour demander le choix d'une autre colonne par une fenêtre secondaire 
    
    fen2=Tk()

    fen2.title("Erreur de jeu !!")
    fen2.focus_set()

    label_error1 =Label(fen2, text=" ")
    label_error1.grid()

    label_error2 =Label(fen2, text="    Choisis une autre colonne, celle-ci est complète.   ")  #message d'annonce d'une erreur 
    label_error2.grid()

    label_error3 =Label(fen2, text=" ")
    label_error3.grid()

    fen2.wm_attributes("-topmost", 1)   #permet un affichage au 1er plan
    fen2.mainloop()

    return

def ajouterPion(co):

    global status
    global J
    e = 3 #épaisseur pion

    global tour

    if status == 1 :

        print("Tour : ", tour)
        
        tour = tour + 1
        
        if tour == 42 :
            fin("Vous êtes à égalité")
            tour = 0

        print("Ajout pion en colonne ", co+1)

        if J[0]==1 and tour/2-tour//2!=0 or J[0]==2 and tour/2-tour//2==0: #test déterminant la couleur du pion suivant le joueur et le tour
            pion='X'
            color='red'
            
        if J[1]==2 and tour/2-tour//2==0 or J[1]==1 and tour/2-tour//2!=0:
            pion='O'
            color='yellow'

        for ligne in range (6,0, -1):
            li = ligne -1
            print("ligne ", li)
            if grille[li][co] == '-' :

                grille[li][co] = pion

                x1 = 250 + 40 * co
                y1 = 100 + 40 * li
                x2 = 250 + 40 * (co+1)
                y2 = 100 + 40 * (li+1)
                dessin.create_oval(x1+e, y1+e, x2-e, y2-e, width=2, outline=color, fill=color)
                break
            
        dessin.update()

        verif()

    return

def verif():

    global grille

    try :
        
        for j in range (0,6) :
            for i in range (0,7) :

                if grille[j][i] == "X" and grille[j][i+1] == "X" and grille[j][i+2] == "X" and grille[j][i+3] == "X":
                    fin("Le joueur aux pions rouges a gagné")
                if grille[j][i] == "X" and grille[j+1][i] == "X" and grille[j+2][i] == "X" and grille[j+3][i] == "X":
                    fin("Le joueur aux pions rouges a gagné")
                if grille[j][i] == "X" and grille[j+1][i+1] == "X" and grille[j+2][i+2] == "X" and grille[j+3][i+3] == "X":
                    fin("Le joueur aux pions rouges a gagné")
                if grille[j][i] == "X" and grille[j+1][i-1] == "X" and grille[j+2][i-2] == "X" and grille[j+3][i-3] == "X":
                    fin("Le joueur aux pions rouges a gagné")
                    
                if grille[j][i] == "O" and grille[j][i+1] == "O" and grille[j][i+2] == "O" and grille[j][i+3] == "O":
                    fin("Le joueur aux pions jaune a gagné")
                if grille[j][i] == "O" and grille[j+1][i] == "O" and grille[j+2][i] == "O" and grille[j+3][i] == "O":
                    fin("Le joueur aux pions jaune a gagné")
                if grille[j][i] == "O" and grille[j+1][i+1] == "O" and grille[j+2][i+2] == "O" and grille[j+3][i+3] == "O":
                    fin("Le joueur aux pions jaune a gagné")
                if grille[j][i] == "O" and grille[j+1][i-1] == "O" and grille[j+2][i-2] == "O" and grille[j+3][i-3] == "O":
                    fin("Le joueur aux pions jaune a gagné")
    except :
        pass

    return

    

def fin (gagant):     #Fonction qui permet l'arrêt du jeu et la fermeture de la fenêtre principale avec affichage d'une fenêtre secondaire

    global fen3
    fen3 = Tk()

    global status

    status = 0

    fen3.title("Fin du jeu")
    fen3.focus_set()

    label_fin1 = Label(fen3, text=" ")
    label_fin1.grid()
    
    label_fin2 = Label(fen3, text=gagant)  #message d'annonce de la fin de la partie
    label_fin2.grid()

    label_fin3 = Label(fen3, text=" ")
    label_fin3.grid()

    fen3.wm_attributes("-topmost", 1)   #permet un affichage au 1er plan
    
    fen3.protocol("WM_DELETE_WINDOW", start_again)
    
    fen3.mainloop()

    return

def start_again():


    global fen3
    global grille
    global fen1
    global tour
    global status

    status = 1

    fen3.destroy()
    grille = [['-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-']]

    tour = 0
    
    fen1.update()
    afficher(grille)

    return

################################### MAIN #######################################

fen1.title("Puissance 4")
fen1.wm_attributes("-topmost", 1) #permet un affichage au 1er plan

dessin = Canvas(fen1, width=800, height=800, bg='dimgrey')
dessin.grid (row = 0, column = 0)

grille = grille()

grille = [['-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-'],
          ['-', '-', '-', '-', '-', '-', '-']]

afficher(grille)

J = joueur()

tour = 0
status = 1

clickPion()

fen1.mainloop()
