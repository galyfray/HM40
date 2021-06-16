import json
import pickle
import subprocess
from abc import ABC, abstractmethod
from typing import Callable, Any, Union

from PIL import Image


class Game(object):
    def __init__(self, name: str = "", run_command: Union['list[str]', str] = "", image=None):
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
        except FileNotFoundError:
            self.image = Image.open("images/default.png")
        self.run_command = data["run_command"]
        return self

    def run(self):
        self._process = subprocess.Popen(self.run_command)

    def is_running(self):
        return self._process is not None and self._process.poll() is None


class GameListListener(ABC):
    @abstractmethod
    def on_game_list_change(self, game_list: "GameList"):
        pass


class GameSorter(object):

    @staticmethod
    def name_sort(game: Game):
        return game.name


class GameFilter(object):
    @staticmethod
    def empty_filter(game: Game) -> bool:
        return True


class GameList(object):

    def __init__(self):
        self._list = []
        self._filter = GameFilter.empty_filter
        self._currentList = []
        self._sorter = GameSorter.name_sort
        self._reverse = False
        self._listeners = []

    def __iter__(self):
        return iter(self._currentList)

    def dump_to_file(self, filename="config/games.json"):
        data = {"filter": pickle.dumps(self._filter).hex(), "sorter": pickle.dumps(self._sorter).hex(),
                "reverse": self._reverse,
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
                    self._update_listeners()
                except json.decoder.JSONDecodeError:
                    self.load_default()
        except FileNotFoundError:
            self.load_default()

    def load_default(self):
        self._list = [Game("Energie 4", ["python3", "Puissance 4/jeu.py"]),
                      Game("Serpent", ["python3", "Snake/snake.py"])]
        self._currentList = self._list.copy()
        self._update_listeners()

    def _load_from_data(self, data: dict):
        if isinstance(data, dict) and "file_version" in data.keys():
            self._list = [Game().deserialize(d) for d in data["games"]]
            self._set_filter(pickle.loads(bytearray.fromhex(data["filter"])))
            self._set_sorter(pickle.loads(bytearray.fromhex(data["sorter"])), data["reverse"])
        else:
            self._list = [Game().deserialize(d) for d in data]
            self._set_filter(self._filter)
            self._set_sorter(self._sorter, self._reverse)

    def _set_filter(self, filter: Callable[[Game], bool]):
        self._filter = filter
        self._currentList = [g if filter(g) else None for g in self._list]
        try:
            while True:
                self._currentList.remove(None)
        except ValueError:
            pass
        self._set_sorter(self._sorter, self._reverse)

    def set_filter(self, filter: Callable[[Game], bool]):
        self._set_filter(filter)
        self._update_listeners()

    def _set_sorter(self, sorter: Callable[[Game], Any], reverse=None):
        if reverse is None:
            reverse = self._reverse
        else:
            self._reverse = reverse
        self._currentList.sort(key=sorter, reverse=reverse)

    def set_sorter(self, sorter: Callable[[Game], Any], reverse=None):
        self._set_sorter(sorter, reverse)
        self._update_listeners()

    def set_reverse(self, reverse: bool):
        self._set_sorter(self._sorter, reverse)
        self._update_listeners()

    def register_listener(self, listener: GameListListener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def _update_listeners(self):
        for li in self._listeners:
            li.on_game_list_change(self)
