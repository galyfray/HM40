import subprocess

from PIL import Image


class Game(object):
    def __init__(self, name: str = "", run_command="", image=None):
        self.name = name
        self.run_command = run_command
        if image is None:
            self.image = Image.open("images/default.png")
        elif isinstance(image, str):
            try:
                self.image = Image.open(image)
            except FileNotFoundError as e:
                self.image = Image.open("images/default.png")

        elif isinstance(image, Image.Image):
            self.image = image
        self._process = None

    def serialize(self) -> dict:
        return {"name": self.name, "run_command": self.run_command,
                "image": self.image.fp.name if self.image is not None else ""}

    def deserialize(self, data: dict) -> None:
        self.name = data["name"]
        try:
            self.image = Image.open(data["image"])
        except FileNotFoundError as e:
            self.image = Image.open("images/default.png")
        self.run_command = data["run_command"]

    def run(self):
        self._process = subprocess.Popen(self.run_command)

    def is_running(self):
        return self._process is not None and self._process.poll() is None
