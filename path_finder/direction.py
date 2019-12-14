import enum
import random


@enum.unique
class Direction(enum.Enum):
    UP = ("U", 0, 1)
    DOWN = ("D", 0, -1)
    LEFT = ("L", -1, 0)
    RIGHT = ("R", 1, 0)

    def __init__(self, letter, x, y):
        self.letter = letter
        self.x = x
        self.y = y


DIRECTIONS = list(Direction)


def random_direction() -> Direction:
    return random.choice(DIRECTIONS)
