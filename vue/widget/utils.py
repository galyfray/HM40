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
