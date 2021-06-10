import os
from tkinter import *

from PIL import ImageTk, Image, ImageDraw


# fonction cambrioler sur la sainte bible de stack overflow
def add_corners(im: Image, rad: int, ) -> Image:
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


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


class RatioKeeperContainer(Frame):
    def __init__(self, root, elem: Widget, ratio, **kw):
        super().__init__(root, **kw)
        self._elem = elem
        self.ratio = ratio

        elem.grid(sticky="nsew", column=0, row=0)

        self.bind("<Configure>", self._on_config, add="+")

    def _on_config(self, event):
        w = event.width
        h = event.height
        rw, rh = get_best_size(self.ratio, w, h)
        ew, eh = self._elem.winfo_width(), self._elem.winfo_height()
        self._elem.place(in_=self, x=(w - rw) / 2, y=(h - rh) / 2,
                         width=rw, height=rh)


def is_in_bound(bound, coord):
    return bound[0] <= coord[0] <= bound[2] and bound[1] <= coord[1] <= bound[3]


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
        while text_bounds[2] - text_bounds[0] > w * 0.95:
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
        for subdir, dirs, files in os.walk("./imageBidon"):
            nb_col = 5
            j = 0
            for file in files:
                filepath = subdir + os.sep + file
                widget = GameWidget(None, Image.open(filepath), file[:file.rfind(".")])
                games_widget.append(widget)

                container = RatioKeeperContainer(self, widget, 0.65)
                container.grid(sticky="nsew", column=j % nb_col, row=j // nb_col, padx=10, pady=10)

                Grid.columnconfigure(self, j % nb_col, weight=1)
                Grid.rowconfigure(self, j // nb_col, weight=1)
                j += 1
        self.game_widgets = games_widget


if __name__ == "__main__":
    fenetre = Tk()
    window = GameGrid(fenetre)
    window.grid(sticky="nsew", column=0, row=0)
    fenetre.rowconfigure(0, weight=1)
    fenetre.columnconfigure(0, weight=1)
    fenetre.geometry('840x640')
    fenetre.mainloop()
