import dataclasses
from enum import Enum
from dataclasses import dataclass
import json
from dataclasses_json import dataclass_json


# x, y
Point = tuple[int, int]


# top left, top right, bottom right, bottom left
SkewedRectangle = tuple[Point, Point, Point, Point]


class Font(str, Enum):
    ARIAL = "arial"
    IMPACT = "impact"


@dataclass
class TextBox:
    bounds: SkewedRectangle
    font: Font
    tag: str


@dataclass
class Meme:
    description: str
    filepath: str
    textboxes: list[TextBox]


@dataclass_json
@dataclass
class Config:
    memes: list[Meme]

    def to_json(self):
        return json.dumps(dataclasses.asdict(self), indent=4)

    def save(self, filepath):
        with open(filepath, "w") as f:
            f.write(self.to_json())


def load(filepath):
    with open(filepath, "r") as f:
        return Config.from_json(f.read())
