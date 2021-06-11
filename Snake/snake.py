import tkinter as tk
from random import randrange



def init():
    global diff, sbSize
    global Serpent, direction
    Serpent = []
    direction = 'bas'
    can.delete('all')
    b1['state'] = tk.NORMAL
    menu = tk.Frame(fen, width=500, height=500)
    txt.set("Cliquez sur 'Lancer' pour commencer le jeu.")

    window = can.create_window(253, 253, window = menu)
    tk.Label(menu, text='Bienvenue sur Snake !', bg='white', font=("arial",30)).grid(row = 0, columnspan=5)
    tk.Label(menu, text='Parametres :', bg='white', font=("arial",20)).grid(row=3, columnspan=5)
    tk.Label(menu, text='Difficulte :', bg='white').grid(row=5, column=0)
    tk.Radiobutton(menu, text='Facile', variable=diff, value=80).grid(column=1, row=5)
    tk.Radiobutton(menu, text='Normal', variable=diff, value=60).grid(column=2, row=5)
    tk.Radiobutton(menu, text='Difficile', variable=diff, value=30).grid(column=3, row=5)
    tk.Radiobutton(menu, text='Hardcore', variable=diff, value=20).grid(column=4, row=5)
    tk.Label(menu, text='Mur', bg='white').grid(row=6, column=0)
    tk.Radiobutton(menu, text='Oui', variable=mur, value=True).grid(column=1, columnspan=2, row=6)
    tk.Radiobutton(menu, text='Non', variable=mur, value=False).grid(column=3, columnspan=2, row=6)
    tk.Label(menu, text='Commencer avec quelle longueur ?', bg='white').grid(row=7, column=0, columnspan=3)
    tk.Spinbox(menu, from_=5, to=100, width=10, textvariable=sbSize).grid(row=7, column=4)



def move():
    global Serpent
    global flag
    can.delete('all')
    i = len(Serpent) - 1
    j = 0
    while i > 0:
        Serpent[i][0] = Serpent[i - 1][0]
        Serpent[i][1] = Serpent[i - 1][1]
        can.create_oval(Serpent[i][0], Serpent[i][1], Serpent[i][0] + dx, Serpent[i][1] + dy, outline='green', fill='black')
        i = i - 1

    can.create_rectangle(pX, pY, pX + dx, pY + dy, outline='white', fill='green')

    if direction == 'gauche':
        Serpent[0][0] = Serpent[0][0] - dx
        if Serpent[0][0] < 10:
            if not mur.get():
                Serpent[0][0] = 493
            else:
                flag = 0

    elif direction == 'droite':
        Serpent[0][0] = Serpent[0][0] + dx
        if Serpent[0][0] > 483:
            if not mur.get():
                Serpent[0][0] = 0
            else:
                flag = 0

    elif direction == 'haut':
        Serpent[0][1] = Serpent[0][1] - dy
        if Serpent[0][1] < 10:
            if not mur.get():
                Serpent[0][1] = 493
            else:
                flag = 0

    elif direction == 'bas':
        Serpent[0][1] = Serpent[0][1] + dy
        if Serpent[0][1] > 483:
            if not mur.get():
                Serpent[0][1] = 0
            else:
                flag = 0

    can.create_oval(Serpent[0][0], Serpent[0][1], Serpent[0][0] + dx, Serpent[0][1] + dy, outline='green', fill='blue')
    test()

    if mur.get():
        can.create_rectangle(0, 0, 500, 10, outline='red', fill='red')
        can.create_rectangle(0, 0, 10, 500, outline='red', fill='red')
        can.create_rectangle(495, 0, 505, 505, outline='red', fill='red')
        can.create_rectangle(0, 495, 505, 505, outline='red', fill='red')

    if flag != 0:
        fen.after(diff.get(), move)
    else:
        gameOver()

def gameOver():
    global Serpent
    can.delete('all')
    del Serpent
    init()


def newGame():
    global pX, pY
    global flag

    b1['state'] = tk.DISABLED
    Serpent.append([x, y])
    for i in range(0, int(sbSize.get())):
        Serpent.append([0, 0])

    txt.set("Score : " + str(len(Serpent)))

    if flag == 0:
        flag = 1
    move()


def left(event):
    global direction
    if direction != 'droite':
        direction = 'gauche'


def right(event):
    global direction
    if direction != 'gauche':
        direction = 'droite'


def up(event):
    global direction
    if direction != 'bas':
        direction = 'haut'


def down(event):
    global direction
    if direction != 'haut':
        direction = 'bas'


def test():
    global pomme
    global flag
    global pX, pY
    global Serpent
    if pX - dx < Serpent[0][0] < pX + dx + 1:
        if pY - dy < Serpent[0][1] < pY + dy + 1:
            # On remet une pomme au hasard
            pX = randrange(20, 465)
            pY = randrange(20, 465)
            # On ajoute un nouveau point au serpent
            Serpent.append([0, 0])
            # print(Serpent)
    for i in range(3, len(Serpent)):
        if Serpent[i][0] - dx < Serpent[0][0] < Serpent[i][0] + dx:
            if Serpent[i][1] - dy < Serpent[0][1] < Serpent[i][1] + dy:
                flag = 0
    txt.set("Score : " + str(len(Serpent)))





x = 250
y = 200
dx, dy = 15, 15
flag = 0



pX = randrange(20, 465)
pY = randrange(20, 465)


fen = tk.Tk()
diff = tk.IntVar(value=60)
mur = tk.BooleanVar()
sbSize = tk.StringVar(value=5)
txt = tk.StringVar()
txt.set("Cliquez sur 'Lancer' pour commencer le jeu.")
can = tk.Canvas(fen, width=500, height=500, bg='black')
can.pack(side=tk.TOP, padx=5, pady=5)








b1 = tk.Button(fen, text='Lancer', command=newGame, bg='black', fg='green')
b1.pack(side=tk.LEFT, padx=5, pady=5)

b2 = tk.Button(fen, text='Quitter', command=fen.destroy, bg='black', fg='green')
b2.pack(side=tk.RIGHT, padx=5, pady=5)

tk.Label(fen, textvariable=txt, bg='black', fg='green', width=40).pack(padx=0, pady=11)

init()

fen.bind('<Right>', right)
fen.bind('<Left>', left)
fen.bind('<Up>', up)
fen.bind('<Down>', down)

fen.mainloop()