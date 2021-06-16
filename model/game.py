import json
import pickle
import subprocess
from typing import Callable, Any

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
                "image": self.image.filename if self.image is not None else ""}

    def deserialize(self, data: dict) -> "Game":
        self.name = data["name"]
        try:
            self.image = Image.open(data["image"])
        except FileNotFoundError as e:
            self.image = Image.open("images/default.png")
        self.run_command = data["run_command"]
        return self

    def run(self):
        self._process = subprocess.Popen(self.run_command)

    def is_running(self):
        return self._process is not None and self._process.poll() is None


class GameList(object):

    def __init__(self):
        self._list = []
        self._filter = lambda e: True
        self._currentList = []
        self._sorter = lambda g: g.name
        self._reverse = False

    def dump_to_file(self, filename="config/games.json"):
        data = {"filter": pickle.dumps(self._filter), "sorter": pickle.dumps(self._sorter), "reverse": self._reverse,
                "games": [g.serialize() for g in self._list], "file_version": "1.0"}

        with open(filename, "w+") as f:
            json.dump(data, f, sort_keys=True, indent=4)
            f.close()

    def load_from_file(self, filename="config/games.json"):
        try:
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                    f.close()
                    self._load_from_data(data)
                except json.decoder.JSONDecodeError:
                    self.load_default()
        except FileNotFoundError:
            self.load_default()

    def load_default(self):
        pass

    def _load_from_data(self, data: dict):
        if "file_version" in data.keys():
            self._list = [Game().deserialize(d) for d in data["games"]]
            self.set_filter(pickle.loads(data["filter"]))
            self.set_sorter(pickle.loads(data["sorter"]), data["reverse"])
        else:
            self._list = [Game().deserialize(d) for d in data]
            self.set_filter(self._filter)
            self.set_sorter(self._sorter, self._reverse)

    def set_filter(self, filter: Callable[[Game], bool]):
        self._filter = filter
        self._currentList = [g if filter(g) else None for g in self._list]
        try:
            while True:
                self._currentList.remove(None)
        except ValueError:
            pass
        self.set_sorter(self._sorter, self._reverse)

    def set_sorter(self, sorter: Callable[[Game], Any], reverse=None):
        if reverse is None:
            reverse = self._reverse
        else:
            self._reverse = reverse
        self._currentList.sort(key=sorter, reverse=reverse)

    def set_reverse(self, reverse: bool):
        self.set_sorter(self._sorter, reverse)
