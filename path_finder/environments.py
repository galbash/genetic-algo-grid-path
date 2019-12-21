"""
Different preset environments to test with
"""
import enum
import math
from path_finder.grid import Cell, Grid, GridWrapper
from path_finder.point import Point


class Size(enum.Enum):
    """
    Available environment sizes
    """

    SMALL = 10
    MEDIUM = 30
    LARGE = 50


def _create_env(size: Size) -> Grid:
    """
    Creates an empty grid
    :param size: The size of the grid to create
    :return: an empty grid of the specified size
    """
    return [[Cell() for _ in range(size.value)] for _ in range(size.value)]


def empty_env(size: Size) -> GridWrapper:
    """
    Returns a default empty environment
    :param size: The size of the environment to create
    :return: an empty environment of the specified size
    """
    grid = _create_env(size)
    return GridWrapper(grid, Point(0, 0), Point(size.value - 1, size.value - 1))


def center_block_env(size: Size, percentage=0.2) -> Grid:
    """
    An environment with a block in the middle
    """
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
    """
    An environment with a row full of blocks except fro the middle cell
    """
    grid = _create_env(size)
    for i in range(0, size.value):
        if i != size.value // 2:
            grid[size.value // 2][i].blocked = True

    return GridWrapper(grid, Point(0, 0), Point(size.value - 1, size.value - 1))


def wall_env(size: Size, space_prec: float = 0.2) -> Grid:
    """
    An environment where the robot has to go around a wall
    """
    grid = _create_env(size)
    for i in range(math.floor(space_prec * size.value), size.value):
        grid[size.value // 2][i].blocked = True

    return GridWrapper(
        grid, Point(size.value - 1, 0), Point(size.value - 1, size.value - 1)
    )


def multi_wall_env(size: Size, space_prec: float = 0.2) -> Grid:
    """
    An environment where the robot has to go around multiple walls
    """
    grid = _create_env(size)
    for i in range(math.floor(space_prec * size.value), size.value):
        grid[size.value // 4][i].blocked = True
        grid[size.value // 2][i].blocked = True
        grid[3 * size.value // 4][i].blocked = True

    return GridWrapper(
        grid, Point(size.value - 1, 0), Point(size.value - 1, size.value - 1)
    )


def multiway_wall_env(size: Size, space_prec: float = 0.2) -> Grid:
    """
    An environment where the robot has to go around multiple walls in multiple
    directions
    """
    grid = _create_env(size)
    for i in range(math.floor(space_prec * size.value), size.value):
        grid[size.value // 4][i].blocked = True
        grid[3 * size.value // 4][i].blocked = True

    for i in range(0, size.value - math.floor(space_prec * size.value)):
        grid[size.value // 2][i].blocked = True

    return GridWrapper(
        grid, Point(size.value - 1, 0), Point(size.value - 1, size.value - 1)
    )


ENVS = {
    env.__name__: env
    for env in [
        empty_env,
        center_block_env,
        peekhole_env,
        wall_env,
        multi_wall_env,
        multiway_wall_env,
    ]
}
