import math
import random
import tkinter as tk
from tkinter import messagebox
import numpy as np
import JeuControle
class Minefield(object):
    fieldWidth=0
    fieldHeight=0
    fieldMines=0
    fieldVeil=0
    reveal = np.array([np.array([' ',' ',' ',' ',' ',' ',' ',' ']),
						np.array([' ',' ',' ',' ',' ',' ',' ',' ']),
						np.array([' ',' ',' ',' ',' ',' ',' ',' ']),
						np.array([' ',' ',' ',' ',' ',' ',' ',' ']),
						np.array([' ',' ',' ',' ',' ',' ',' ',' ']),
						np.array([' ',' ',' ',' ',' ',' ',' ',' ']),
						np.array([' ',' ',' ',' ',' ',' ',' ',' ']),
						np.array([' ',' ',' ',' ',' ',' ',' ',' '])])
    field = np.array([np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
                       np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
                       np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
                       np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
                       np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
                       np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
                       np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']),
                       np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])])

    def __init__(self, width, height, mines): #Constructeur
        self.fieldWidth = width
        self.fieldHeight = height
        self.fieldMines = mines
        self.fieldVeil = width*height-mines
        #créé le terrain de jeu
        for i in range(self.fieldWidth):
            for j in range(self.fieldHeight):
                print(str(i) + "|" + str(j))
                self.field[i][j] = "0"
                self.reveal[i][j] = "1"
        #place les mines
        placed=0
        while placed < mines:
            x = math.floor(random.random() * self.fieldWidth)
            y = math.floor(random.random() * self.fieldHeight)
            if self.field[x][y] == '0':
                self.field[x][y] = 'x'
                placed=placed+1
        #définie le nombre de mines voisines
        for x in range(self.fieldWidth) :
            for y in range(self.fieldHeight):
                if self.field[x][y] == '0':
                    count = 0
                    for dx in (-1,0,1):
                        for dy in (-1, 0, 1):
                            x0 = x + dx
                            y0 = y + dy
                            if 0 <= x0 < self.fieldWidth and 0 <= y0 < self.fieldHeight:
                                    if self.field[x0][y0] == 'x':
                                        count=count+1
                    self.field[x][y] = count


    def get_width(self):
        return self.fieldWidth
    def get_height(self):
        return self.fieldHeight

    def Clicked(self):
        return messagebox.showinfo("Hello Python", "Hello World")

    def get_reaveled(self):
        self.fieldVeil=0
        width=self.fieldWidth
        height=self.fieldHeight
        for i in range(width):
            for j in range(height):
                if self.reveal[i][j]=="1":
                    self.fieldVeil=self.fieldVeil+1
        return self.fieldVeil

    def get_explosions(self):
        reveal = self.reveal
        field = self.field
        width = self.fieldWidth
        height = self.fieldHeight
        count = 0
        for i in range(width):
            for j in range(height):
                if reveal[i][j] == "0" and field[i][j] == "x":
                    count = count + 1
        return count
    #A faire
    #Retourne le symbole de la case
    def number(self, x,y):
        x0=x
        y0=y

        if 0 <= x0 < self.fieldWidth and 0 <= y0 < self.fieldHeight and self.reveal[x0][y0]=="0":
            return self.field[x0][y0]
        else:
            return " "

    def revelation(self, x, y):
        xbis=x
        ybis=y
        print("Click on : ")
        print("x:"+str(xbis)+"y:"+str(xbis))
        #Vérif
        if xbis<0 or xbis> self.fieldWidth or ybis<0 or ybis>self.fieldHeight:
            print("pb vérif")
            return
        if self.reveal[xbis][ybis]=="0":
            print("pb reveal")
            return
        tiles = [xbis,ybis]
        print("Tiles:")
        print(tiles)
        while len(tiles)>0:
            y0=tiles.pop()
            x0=tiles.pop()
            print("Tiles après Pop:")
            print(tiles)
            print(str(x0) + "/" + str(y0))
            self.reveal[x0][y0] = "0"
            if self.field[x0][y0] == '0':
                for dx in (-1,0,1):
                    for dy in (-1,0,1):
                        x1=x0+dx
                        y1=y0+dy
                        print("vérif de :")
                        print(str(x1) + "/" + str(y1))
                        if 0<=x1<self.fieldWidth and 0<=y1<self.fieldHeight and self.reveal[x1][y1]=="1":

                            tiles.append(x1)
                            tiles.append(y1)
                            print("Tiles fin for:")
                            print(tiles)


    def toView(self,fen):
        for y in range(self.fieldHeight):
            for x in range(self.fieldWidth):
                if self.reveal[x][y]=="0":
                    bouton = tk.Button(fen, text=str(self.field[x][y]), relief=tk.GROOVE)
                    bouton.grid(row=x, column=y)
                else:
                    bouton = tk.Button(fen,text="  ", fg="white", bg="white" , command= lambda i=x, j=y: JeuControle.hit(i,j), relief=tk.RAISED)
                    bouton.grid(row=x, column=y)
        print("Nombre de cases caché")
        print(self.get_reaveled())
        print("Nombre d'explosions:")
        print(self.get_explosions())

