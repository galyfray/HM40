from tkinter import *


def get_best_size(wanted_ratio, w, h):
    c_ratio = w / h
    rw, rh = w, h
    if wanted_ratio < c_ratio:
        rw = w / c_ratio
        rw *= wanted_ratio
        rw = int(rw)
    else:
        rh = h * c_ratio
        rh /= wanted_ratio
        rh = int(rh)
    return rw, rh


class GameManager(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._playerTurn = 1
        self._container = RatioKeeperContainer(self, 1)
        self._board = Board(self, self._container, 840, 640)
        self._container.pack(fill=BOTH, expand=YES)
        self._label = None

    def get_player_turn(self):
        return self._playerTurn

    def end_player_turn(self):
        if self._playerTurn == 0:
            return
        self._playerTurn = 2 if self._playerTurn == 1 else 1

    def end_game(self, tie: bool = False):
        if self._playerTurn == 0:
            return
        text = ""
        if tie:
            text = "No body win this is a tie !"
        else:
            text = f"Player {self._playerTurn} Win !"
        text += "\nclick here to play again"
        self._label = Label(self, text=text, justify=CENTER,
                            font=("TkDefaultFont", int(self._container.winfo_width() * 0.03)))
        self._label.lift(self._container)
        self._label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self._label.bind("<Button-1>", self._on_click)

        self._playerTurn = 0

    def _on_click(self, event):
        self._label.destroy()
        self._container.destroy()
        self._board.destroy()
        self._playerTurn = 1
        self._container = RatioKeeperContainer(self, 1)
        self._board = Board(self, self._container, 840, 640)
        self._container.pack(fill=BOTH, expand=YES)


class Cell(Frame):
    def __init__(self, turnmanager: GameManager, master):
        super().__init__(master)
        self.manager = turnmanager
        self.state = 0
        self.canvas = Canvas(self, bd=0, bg="white", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.bind("<Button-1>", self.on_click)

        self.bind("<Configure>", self.on_resize)

        self.R = True

    def on_resize(self, event):
        self.re_draw()

    def on_click(self, event):
        if self.state != 0:
            return
        self.state = self.manager.get_player_turn()
        self.re_draw()

    def re_draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), width=10)
        if self.state == 1:
            self.canvas.create_oval(0, 0, self.winfo_width(), self.winfo_height(), width=10)
        elif self.state == 2:
            self.canvas.create_line(0, 0, self.winfo_width(), self.winfo_height(), width=10)
            self.canvas.create_line(self.winfo_width(), 0, 0, self.winfo_height(), width=10)


class Board(Frame):
    def __init__(self, turn_manager: GameManager, master, width: int, height: int):
        s = min(width, height)
        super().__init__(master, width=s, height=s)
        self.manager = turn_manager
        self.cell_grid = []

        for i in range(3):
            self.cell_grid.append([])
            for j in range(3):
                cell = Cell(turn_manager, self)
                self.cell_grid[i].append(cell)
                cell.grid(column=i, row=j, padx=0, pady=0, sticky="nsew")
                self.rowconfigure(j, weight=1)
                cell.canvas.bind("<Button-1>", self.on_click, add="+")
            self.columnconfigure(i, weight=1)

    def on_click(self, event):
        self.check_win()
        self.manager.end_player_turn()

    def check_win(self):
        for i in range(len(self.cell_grid)):
            if self.are_same(self.cell_grid[i]):
                self.manager.end_game()
                return
            if self.are_same([self.cell_grid[j][i] for j in range(3)]):
                self.manager.end_game()
                return

        if self.are_same([self.cell_grid[j][j] for j in range(3)]):
            self.manager.end_game()
            return

        if self.are_same([self.cell_grid[2 - j][j] for j in range(3)]):
            self.manager.end_game()
            return

        for i in range(3):
            for j in range(3):
                if self.cell_grid[i][j].state == 0:
                    return
        self.manager.end_game(True)

    @staticmethod
    def are_same(cell_list: list) -> bool:
        e = cell_list[0].state
        if e == 0:
            return False
        for c in cell_list[1:]:
            if c.state != e:
                return False
        return True


class RatioKeeperContainer(Frame):
    def __init__(self, root, ratio, **kw):
        super().__init__(root, **kw)
        self._ratio = ratio

        self.bind("<Configure>", self._on_config, add="+")

    def _on_config(self, event):
        w = event.width
        h = event.height
        self._place_elem(w, h)

    def set_ratio(self, ratio: float):
        self._ratio = ratio
        self._place_elem(self.winfo_width(), self.winfo_height())

    def _place_elem(self, w: int, h: int):
        elem = self.winfo_children()[0]
        if elem is not None:
            rw, rh = get_best_size(self._ratio, w, h)
            elem.place(in_=self, x=(w - rw) / 2, y=(h - rh) / 2,
                       width=rw, height=rh)


if __name__ == "__main__":
    fenetre = Tk()

    gm = GameManager(fenetre, bg="grey")
    gm.pack(fill=BOTH, expand=YES)

    fenetre.geometry('840x640')
    fenetre.mainloop()
