import tkinter as tk

from PIL import Image, ImageTk


class Interface(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ____________Frame Menu_____________

        # ___Image___
        self.image_logo = Image.open("images/big_logo.png")
        self.image_logo = self.image_logo.resize((160, 140))
        self.img = ImageTk.PhotoImage(self.image_logo)
        logo = tk.Label(self, image=self.img)
        # logo.grid(row=0, sticky=tk.W)
        logo.pack(side="top", fill="both", expand="yes")
        # ___Frame Label Trier par___
        Trier_par = tk.LabelFrame(self, text="Trier par")
        # ___Buttons Radio___

        tri = tk.IntVar(value=1)

        tk.Radiobutton(Trier_par, text="Ordre Alphabétique", indicatoron=0, background="light blue", width=20, padx=20,
                       variable=tri, value=1).grid(row=0, sticky=tk.W)
        tk.Radiobutton(Trier_par, text="Plus récent", indicatoron=0, background="light blue", width=20, padx=20,
                       variable=tri, value=2).grid(row=1, sticky=tk.W)
        tk.Radiobutton(Trier_par, text="Plus joué", indicatoron=0, background="light blue", width=20, padx=20,
                       variable=tri,
                       value=3).grid(row=2, sticky=tk.W)
        tk.Radiobutton(Trier_par, text="Moins joué", indicatoron=0, background="light blue", width=20, padx=20,
                       variable=tri, value=4).grid(row=3, sticky=tk.W)

        Trier_par.pack()

        # ___Button Fonctionnalitées___
        button_Jeu_aleatoire = tk.Button(self, text="Jeu aléatoire")
        button_Jeu_aleatoire.pack(fill=tk.BOTH, expand=tk.YES)
        button_Autre_Fonction = tk.Button(self, text="Autre Fonctions...")
        button_Autre_Fonction.pack(fill=tk.BOTH, expand=tk.YES)

        """

    
        #def __init__(self):
        """


if __name__ == "__main__":
    # main Pour tester l'interface
    root = tk.Tk()
    interface = Interface(root, borderwidth=10, background="dark blue")
    interface.grid(row=0, column=0, sticky="E")
    root.mainloop()
