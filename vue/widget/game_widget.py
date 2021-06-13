import os

from PIL import ImageTk

from utils import *


class GameWidget(Frame):
    def __init__(self, root, background_image: Image, name: str, **kw):
        super().__init__(root, **kw)
        self.image_map = {"_base": background_image}
        self.image_map["_main"] = ImageTk.PhotoImage(self.image_map["_base"])
        self.image_map["base_play"] = Image.open("./play-button.png")
        self._mouse = False

        self._canvas = Canvas(self, bd=0, highlightthickness=0)
        self._canvas.pack(fill=BOTH, expand=1)

        self.name = name

        self._click_map = {}

        self.bind("<Configure>", self._on_config, add="+")
        self.bind("<Enter>", self.on_enter, add="+")
        self.bind("<Leave>", self.on_leave, add="+")
        self._canvas.bind("<Button-1>", self._on_click, add="+")

    def _on_config(self, event):
        self.re_draw()

    def re_draw(self):
        self._canvas.delete('all')
        self._click_map = {}
        w, h = self.winfo_width(), self.winfo_height()

        iw, ih = self.image_map["_base"].size
        rw, rh = get_best_size(w / h, iw, ih)

        x_border = iw - rw
        y_border = ih - rh

        start = (x_border / 2, y_border / 2)
        end = (start[0] + rw, start[1] + rh)

        self.image_map["_main"] = self.image_map["_base"].crop((*start, *end)).resize((w, h))
        self.image_map["_main"].putalpha(Image.new('L', self.image_map["_main"].size, 255))

        overlay = Image.new('RGBA', self.image_map["_main"].size, (0, 0, 0, 0))

        draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
        draw.rectangle(((0, int(h * (0.6 if self._mouse else 0.8))), (w, h)), fill=(50, 50, 50, 200))

        self.image_map["_main"] = Image.alpha_composite(self.image_map["_main"], overlay)

        self.image_map["_main"] = ImageTk.PhotoImage(add_corners(self.image_map["_main"],
                                                                 max(int(w * 0.1), int(h * 0.1))))
        self._canvas.create_image((w / 2, h / 2), image=self.image_map["_main"])
        text = self.name
        text_elem = self._canvas.create_text(int(w / 2), int((0.7 if self._mouse else 0.9) * h), fill="white",
                                             font=f"Times {int(h * 0.1)} italic bold",
                                             text=text, anchor="center")
        text_bounds = self._canvas.bbox(text_elem)
        while text_bounds[2] - text_bounds[0] > w * 0.95 and len(text) > 3:
            text = text[:-4] + "..."
            self._canvas.itemconfigure(text_elem, text=text)
            text_bounds = self._canvas.bbox(text_elem)

        if self._mouse:
            s = int(min(h, w) * 0.25)
            self.image_map["_play"] = ImageTk.PhotoImage(self.image_map["base_play"].resize((s, s)))
            img = self._canvas.create_image((int(w - 0.6 * s), int(text_bounds[3] + 0.5 * s)),
                                            image=self.image_map["_play"])
            self._click_map[self._canvas.bbox(img)] = self.run_game

    def on_enter(self, event):
        self._mouse = True
        self.re_draw()

    def on_leave(self, event):
        self._mouse = False
        self.re_draw()

    def run_game(self, event):
        print("the game is running")

    def _on_click(self, event):
        for elem in self._click_map.keys():
            if is_in_bound(elem, (event.x, event.y)):
                self._click_map[elem](event)


class GameGrid(Frame):
    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        games_widget = []
        containers = []
        self._nb_col = 5
        self._ratio = 0.65
        self._nb_row = 0
        for subdir, dirs, files in os.walk("./imageBidon"):
            for file in files:
                filepath = subdir + os.sep + file
                container = RatioKeeperContainer(self, 0.65)
                widget = GameWidget(container, Image.open(filepath), file[:file.rfind(".")])
                games_widget.append(widget)
                containers.append(container)
        self.game_widgets = games_widget
        self.containers = containers
        self._place_containers()

    def _place_containers(self):
        self._nb_row = 0
        j = 0
        for container in self.containers:
            container.grid(sticky="nsew", column=j % self._nb_col, row=j // self._nb_col, padx=10, pady=10)
            Grid.columnconfigure(self, j % self._nb_col, weight=1, uniform="filled")
            Grid.rowconfigure(self, j // self._nb_col, weight=1, uniform="filled")
            j += 1
        self._nb_row = j // self._nb_col

    def _reset_grid(self):
        j = 0
        for container in self.containers:
            container.grid_forget()
            Grid.columnconfigure(self, j % self._nb_col, weight=0, uniform="empty")
            Grid.rowconfigure(self, j // self._nb_col, weight=0, uniform="empty")
            j += 1

    def get_nb_row(self):
        return self._nb_row

    def set_nb_col(self, nb_col: int):
        self._reset_grid()
        self._nb_col = nb_col
        self._place_containers()

    def get_nb_col(self):
        return self._nb_col

    def get_ratio(self):
        return self._ratio


if __name__ == "__main__":
    root = Tk()
    root.configure(background='black')
    sf = ScrollableFrame(root)

    cr = GameGrid(sf)
    cr.grid(sticky="nsew")


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
    sf.grid(column=0, row=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('840x640')
    root.mainloop()
