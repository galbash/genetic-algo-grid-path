import math

from path_finder.grid import Point


def distance(p1: Point, p2: Point) -> int:
    return int(math.fabs(p1[0] - p2[0]) + math.fabs(p1[1] - p2[1]))
