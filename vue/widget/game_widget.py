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


class GameWidget(Frame):
    def __init__(self, root, background_image: Image, name: str, **kw):
        super().__init__(root, **kw)

        self._base_image = background_image
        self._image = ImageTk.PhotoImage(self._base_image)
        self._mouse = False

        self._canvas = Canvas(self, bd=0, highlightthickness=0)
        self._canvas.pack(fill=BOTH, expand=1)

        self.name = name

        self.bind("<Configure>", self._on_config, add="+")
        self.bind("<Enter>", self.on_enter, add="+")
        self.bind("<Leave>", self.on_leave, add="+")

    def _on_config(self, event):
        self.re_draw()

    def re_draw(self):
        self._canvas.delete('all')
        w, h = self.winfo_width(), self.winfo_height()

        iw, ih = self._base_image.size
        rw, rh = get_best_size(w / h, iw, ih)

        x_border = iw - rw
        y_border = ih - rh

        start = (x_border / 2, y_border / 2)
        end = (start[0] + rw, start[1] + rh)

        self._image = self._base_image.crop((*start, *end)).resize((w, h))
        self._image.putalpha(Image.new('L', self._image.size, 255))

        overlay = Image.new('RGBA', self._image.size, (0, 0, 0, 0))

        draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
        draw.rectangle(((0, int(h * (0.5 if self._mouse else 0.8))), (w, h)), fill=(50, 50, 50, 200))

        self._image = Image.alpha_composite(self._image, overlay)

        self._image = ImageTk.PhotoImage(add_corners(self._image,
                                                     max(int(w * 0.1), int(h * 0.1))))
        self._canvas.create_image((w / 2, h / 2), image=self._image)
        text = self.name
        text_elem = self._canvas.create_text(int(w / 2), int((0.6 if self._mouse else 0.9) * h), fill="white",
                                             font=f"Times {int(h * 0.1)} italic bold",
                                             text=text, anchor="center")
        text_bounds = self._canvas.bbox(text_elem)
        while text_bounds[2] - text_bounds[0] > w * 0.95:
            text = text[:-4] + "..."
            self._canvas.itemconfigure(text_elem, text=text)
            text_bounds = self._canvas.bbox(text_elem)

        if self._mouse:
            button = Button(text="Start", font=f"Times {int(h * 0.08)} italic bold", justify='center',
                            command=lambda e: print("click"))
            button.place()

    def on_enter(self, event):
        self._mouse = True
        self.re_draw()

    def on_leave(self, event):
        self._mouse = False
        self.re_draw()


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
    # window.pack(fill=BOTH, expand=1)
    fenetre.geometry('840x640')
    fenetre.mainloop()
