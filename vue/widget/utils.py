from tkinter import *

from PIL import Image, ImageDraw


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


def is_in_bound(bound, coord):
    return bound[0] <= coord[0] <= bound[2] and bound[1] <= coord[1] <= bound[3]


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


class ScrollableFrame(Frame):
    def __init__(self, master=None, *args, **kwargs):
        self.container = Frame(master)
        self._canvas = Canvas(self.container)

        self.scrollbar = Scrollbar(self.container, orient="vertical", command=self.set_yview)

        super().__init__(self._canvas, *args, **kwargs)

        self.bind("<Configure>", self._on_config)

        self._canvas.bind("<Configure>", self._on_canvas_config, add="+")

        self._canvas.configure(yscrollcommand=self.scrollbar.set)

        self._canvas.grid(sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

    def pack(self, *args, **kwargs):
        return self.container.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        return self.container.grid(*args, **kwargs)

    def _on_config(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_config(self, event):
        self._canvas.delete("all")
        self._canvas.create_window((0, 0), window=self, anchor="nw", width=event.width)

    def set_yview(self, *args):
        yview = [i for i in args]
        yview[1] = yview[1] if float(yview[1]) > 0 else "0.0"
        return self._canvas.yview(*yview)
