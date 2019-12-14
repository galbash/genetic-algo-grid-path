import enum
import math
from path_finder.grid import Cell, Grid, Point, GridWrapper


class Size(enum.Enum):
    SMALL = 10
    MEDIUM = 30
    LARGE = 50


def _create_env(size: Size) -> Grid:
    return [[Cell() for _ in range(size.value)] for _ in range(size.value)]


def empty_env(size: Size) -> GridWrapper:
    grid = _create_env(size)
    return GridWrapper(grid, Point(0, 0), Point(size.value - 1, size.value - 1))


def center_block_env(size: Size, percentage=0.2) -> Grid:
    block_size = (size.value ** 2) * percentage
    side_size = math.sqrt(block_size)
    half_size_size = int(side_size // 2)
    grid = _create_env(size)
    for i in range(size.value // 2 - half_size_size, size.value // 2 + half_size_size):
        for j in range(
            size.value // 2 - half_size_size, size.value // 2 + half_size_size
        ):
            grid[i][j].blocked = True
    return GridWrapper(grid, Point(0, 0), Point(size.value - 1, size.value - 1))


def peekhole_env(size: Size) -> Grid:
    grid = _create_env(size)
    for i in range(0, size.value):
        if i != size.value // 2:
            grid[size.value // 2][i].blocked = True

    return GridWrapper(grid, Point(0, 0), Point(size.value - 1, size.value - 1))


def wall_env(size: Size, space_prec: float = 0.2) -> Grid:
    grid = _create_env(size)
    for i in range(math.floor(space_prec * size.value), size.value):
        grid[size.value // 2][i].blocked = True

    return GridWrapper(
        grid, Point(size.value - 1, 0), Point(size.value - 1, size.value - 1)
    )
