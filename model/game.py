import json
import os
import pickle
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Any, Union

from PIL import Image


class GameEvent(Enum):
    TAG_CHANGE: 1
    NAME_CHANGE: 2
    COMMAND_CHANGE: 3


class GameEventListener(ABC):
    @abstractmethod
    def on_game_event(self, game: "Game", event: GameEvent):
        pass


class Game(object):
    def __init__(self, name: str = "", run_command: Union['list[str]', str] = "", image=None, tags=None):
        if tags is None:
            tags = []
        self._name = name
        self._tags = tags
        self._run_command = run_command
        self._listeners = []
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
        return {"name": self._name, "run_command": self._run_command,
                "image": self.image.filename if self.image is not None else "",
                "tags": self._tags}

    def deserialize(self, data: dict) -> "Game":
        self._name = data["name"]
        try:
            self.image = Image.open(data["image"])
        except FileNotFoundError:
            self.image = Image.open("images/default.png")
        self._run_command = data["run_command"]
        if "tags" in data.keys():
            self._tags = sorted(data["tags"])

        return self

    def register_listener(self, listener: GameEventListener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def run(self):
        self._process = subprocess.Popen(self._run_command)

    def is_running(self):
        return self._process is not None and self._process.poll() is None

    def get_tags(self) -> "list[str]":
        return self._tags.copy()

    def add_tag(self, tag: str):
        if tag not in self._tags:
            self._tags.append(tag)
            self._tags.sort()

    def get_name(self) -> str:
        return self._name

    def remove_tag(self, tag: str):
        self._tags.remove(tag)
        self._tags.sort()

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False

        if self._name != other.get_name():
            return False

        if self._tags != other._tags:
            return False

        if self._run_command != other._run_command:
            return False

        if self.image != other.image:
            return False

        return True


class GameListListener(ABC):
    @abstractmethod
    def on_game_list_change(self, game_list: "GameList"):
        pass


class GameSorter(object):

    @staticmethod
    def name_sort(game: Game):
        return game.get_name()


class GameFilter(object):
    @staticmethod
    def empty_filter(game: Game) -> bool:
        return True


class GameList(GameEventListener):

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

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError:  # Guard against race condition
                return

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
                    for g in self._list:
                        g.register_listener(self)
                    self._update_listeners()
                except json.decoder.JSONDecodeError:
                    self.load_default()
        except FileNotFoundError:
            self.load_default()

    def load_default(self):
        self._list = [Game("Energie 4", ["python3", "Puissance 4/jeu.py"]),
                      Game("Serpent", ["python3", "Snake/snake.py"])]
        self._currentList = self._list.copy()
        for g in self._list:
            g.register_listener(self)
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
        self._set_sorter(self._sorter)
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

    def on_game_event(self, game: Game, event: GameEvent):
        self.set_filter(self._filter)

    def add_game(self, game: Game):
        if game not in self._list:
            self._list.append(game)
            game.register_listener(self)
