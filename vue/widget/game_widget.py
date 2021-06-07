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


class GameWidget(Frame):
    def __init__(self, root, background_image: Image, name: str, **kw):
        super().__init__(root, **kw)

        self._base_image = background_image
        self._image = ImageTk.PhotoImage(self._base_image)

        self.canvas = Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        self.name = name

        self.bind("<Configure>", self._on_config, add="+")

    def _on_config(self, event):
        self.re_draw()

    def re_draw(self):
        self.canvas.delete('all')
        w, h = self.winfo_width(), self.winfo_height()
        iw, ih = self._base_image.size
        ratios = (h / w, ih / iw)
        rw, rh = iw, ih
        if ratios[0] > ratios[1]:
            rw = iw * ratios[1]
            rw /= ratios[0]
            rw = int(rw)
        else:
            rh = ih / ratios[1]
            rh *= ratios[0]
            rh = int(rh)

        x_border = iw - rw
        y_border = ih - rh

        start = (x_border / 2, y_border / 2)
        end = (start[0] + rw, start[1] + rh)

        self._image = self._base_image.crop((*start, *end)).resize((w, h))
        self._image.putalpha(Image.new('L', self._image.size, 255))

        overlay = Image.new('RGBA', self._image.size, (0, 0, 0, 0))

        draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
        draw.rectangle(((0, int(h * 0.8)), (w, h)), fill=(50, 50, 50, 200))

        self._image = Image.alpha_composite(self._image, overlay)

        self._image = ImageTk.PhotoImage(add_corners(self._image,
                                                     max(int(w * 0.1), int(h * 0.1))))
        self.canvas.create_image((w / 2, h / 2), image=self._image)
        self.canvas.create_text(int(w / 2), int(0.9 * h), fill="white", font=f"Times {int(h * 0.1)} italic bold",
                                text=self.name, anchor="center")


class GameGrid(Frame):
    def __init__(self, root, **kw):
        super().__init__(root, **kw)
        games_widget = []
        for subdir, dirs, files in os.walk("./imageBidon"):
            i = int(len(files) ** 0.5)
            j = 0
            for file in files:
                # print os.path.join(subdir, file)
                filepath = subdir + os.sep + file
                widget = GameWidget(self, Image.open(filepath), file[:file.rfind(".")])
                games_widget.append(widget)
                widget.grid(sticky="nswe", column=j % i, row=j // i, padx=10, pady=10)
                Grid.columnconfigure(self, j % i, weight=1)
                Grid.rowconfigure(self, j // i, weight=1)
                j += 1
        self.game_widgets = games_widget


if __name__ == "__main__":
    fenetre = Tk()
    window = GameGrid(fenetre)
    window.pack(fill=BOTH, expand=1)
    fenetre.geometry('840x640')
    fenetre.mainloop()
