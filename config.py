import dataclasses
from enum import Enum
from dataclasses import dataclass
import json


# x, y
Point = tuple[int, int]


class Font(str, Enum):
    ARIAL = "arial"
    IMPACT = "impact"


# top left, top right, bottom right, bottom left
SkewedRectangle = tuple[Point, Point, Point, Point]


@dataclass
class TextBox:
    bounds: SkewedRectangle
    font: Font


class Caption:
    pass


TextLayout = Caption | list[TextBox]


@dataclass
class Meme:
    description: str
    filepath: str
    text_layout: TextLayout


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
        return Config(**json.load(f))
