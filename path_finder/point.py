"""
A point in the grid
"""
import math
from collections import namedtuple

from functools import lru_cache

Point = namedtuple("Point", "x y")


@lru_cache()
def distance(p1: Point, p2: Point) -> int:
    """
    Calculate the distance between two points
    :param p1: The source point
    :param p2: The target point
    :return: The distance in cells (no diagonals)
    """
    return int(math.fabs(p1[0] - p2[0]) + math.fabs(p1[1] - p2[1]))
