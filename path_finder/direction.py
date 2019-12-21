"""
Directions the robot can move in
"""
import enum
import random


@enum.unique
class Direction(enum.Enum):
    """
    An enum representing available directions
    """

    UP = ("U", 0, 1, "↑")
    DOWN = ("D", 0, -1, "↓")
    LEFT = ("L", -1, 0, "←")
    RIGHT = ("R", 1, 0, "→")

    def __init__(self, letter, x, y, icon):
        """
        :param letter: A letter for pretty-printing the direction
        :param x: The change in the x co-ordinate in order to move in this direction
        :param y: The change in the y co-ordinate in order to move in this direction
        :param icon: An ascii icon for pretty-printing the direction
        """
        self.letter = letter
        self.x = x
        self.y = y
        self.icon = icon


DIRECTIONS = list(Direction)


def random_direction() -> Direction:
    """
    :return: a random direction from the available directions list
    """
    return random.choice(DIRECTIONS)
