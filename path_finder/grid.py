from typing import Sequence
from path_finder.chromosome import Chromosome
from collections import namedtuple


class Cell:
    def __init__(self, blocked=False):
        self.blocked = blocked


Point = namedtuple("Point", "x y")
Grid = Sequence[Sequence[Cell]]


def simulate_movement(grid: Grid, start: Point, steps: Chromosome) -> Point:
    grid_x_size = len(grid[0])
    grid_y_size = len(grid)
    if start.y < 0 or start.x < 0 or start.y >= grid_y_size or start.x >= grid_x_size:
        raise ValueError("invalid start point", start)
    if grid[start.y][start.x].blocked:
        raise ValueError("initial point occupied")

    current = start
    for step in steps:
        next = Point(current.x + step.x, current.y + step.y)
        if next.y < 0 or next.x < 0 or next.y >= grid_y_size or next.x >= grid_x_size:
            continue
        if grid[next.y][next.x].blocked:
            continue

        current = next

    return current
