"""
The grid the robot is moving on
"""
from typing import Sequence, Iterable
from itertools import islice
from path_finder.direction import Direction
from path_finder.chromosome import Chromosome
from terminaltables import SingleTable
from methodtools import lru_cache

from path_finder.point import Point, distance


class Cell:
    def __init__(self, blocked=False):
        self.blocked = blocked


Grid = Sequence[Sequence[Cell]]


def chunk(it: Iterable, size: int) -> Iterable:
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


class GridWrapper:
    """
    A wrapper for the grid which defines the problem environment:
      - grid
      - start
      - target
    """

    def __init__(self, grid: Grid, start: Point, target: Point):
        """
        :param grid: The grid to use
        :param start: The starting point on the grid
        :param target: The target point on the grid
        """
        self.grid = grid
        self.grid_x_size = len(grid[0])
        self.grid_y_size = len(grid)
        self.start = start
        self.target = target

        if not self._check_point(start):
            raise ValueError("invalid start point", start)
        if not self._check_point(target):
            raise ValueError("invalid target point", target)

    def _check_point(self, point) -> bool:
        """
        Checks that a point is accessible on the grid
        :param point: The point to check
        """
        if (
            point.y < 0
            or point.x < 0
            or point.y >= self.grid_y_size
            or point.x >= self.grid_x_size
        ):
            return False
        if self.grid[point.y][point.x].blocked:
            return False
        return True

    def _next_point(self, current: Point, step: Direction):
        """
        Finds the step result
        :param current: Current point on the grid
        :param step: The direction we are moving in
        :return: The next point on the grid
        """
        next = Point(current.x + step.x, current.y + step.y)
        if not self._check_point(next):
            return current

        return next

    @lru_cache()
    def _simulate_movement(self, start: Point, steps: tuple) -> Point:
        """
        Simulates the movement of a series of steps on the grid
        :param start: The start point
        :param steps: The series of steps
        :return: the point we stop in
        """
        current = start
        for step in steps:
            current = self._next_point(current, step)

            if current == self.target: # short-circut
                break

        return current

    def simulate_movement(self, steps: Chromosome) -> Point:
        """
        Simulates the movement of a chromosome on the grid
        :param steps: The series of steps
        :return: the point we stop in
        """
        current = self.start
        for c in chunk(steps, 25):
            current = self._simulate_movement(current, tuple(c))
            if current == self.target: # short-circut
                break

        return current

    def calculate_distance(self, steps: Chromosome) -> int:
        """
        Calculates the distance of the robot from the target after performint hte
        steps dictated by the chromosome
        :param steps: The chromosome
        :return: the distance to the target
        """
        current = self.simulate_movement(steps)
        return distance(current, self.target)

    def to_table(self, path: Chromosome = None) -> SingleTable:
        """
        Converts a grid to a textual table
        :param path: optional path to draw on the grid
        :return: a SingleTable object
        """
        table_data = [
            ["*" if cell.blocked else "" for cell in row] for row in self.grid
        ]

        if path:
            current = self.start
            for step in path:
                table_data[current.y][current.x] = step.icon
                current = self._next_point(current, step)
                if current == self.target: # short-circut
                    break

        if self.start:
            table_data[self.start.y][self.start.x] = "S"

        if self.target:
            table_data[self.target.y][self.target.x] = "T"

        table = SingleTable(table_data[::-1])
        table.inner_row_border = True
        return table

    def __str__(self) -> str:
        return self.to_table().table + "\n"
