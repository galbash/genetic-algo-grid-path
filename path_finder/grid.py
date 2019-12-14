from typing import Sequence
from path_finder.direction import Direction
from path_finder.chromosome import Chromosome
from collections import namedtuple
from terminaltables import SingleTable


class Cell:
    def __init__(self, blocked=False):
        self.blocked = blocked


Point = namedtuple("Point", "x y")
Grid = Sequence[Sequence[Cell]]


class GridWrapper:
    def __init__(self, grid: Grid, start: Point, target: Point):
        self.grid = grid
        self.grid_x_size = len(grid[0])
        self.grid_y_size = len(grid)
        self.start = start
        self.target = target

        self.validate_point(grid, start)
        self.validate_point(grid, target)

    def validate_point(self, grid, point):
        if (
            point.y < 0
            or point.x < 0
            or point.y >= self.grid_y_size
            or point.x >= self.grid_x_size
        ):
            raise ValueError("invalid point", point)
        if grid[point.y][point.x].blocked:
            raise ValueError("point occupied")

    def _next_point(self, current: Point, step: Direction):
        next = Point(current.x + step.x, current.y + step.y)
        if (
            next.y < 0
            or next.x < 0
            or next.y >= self.grid_y_size
            or next.x >= self.grid_x_size
        ):
            return current
        if self.grid[next.y][next.x].blocked:
            return current

        return next

    def simulate_movement(self, steps: Chromosome) -> Point:
        current = self.start
        for step in steps:
            current = self._next_point(current, step)

        return current

    def to_table(self, path: Chromosome = None) -> SingleTable:
        table_data = [
            ["*" if cell.blocked else "" for cell in row] for row in self.grid
        ]

        if path:
            current = self.start
            for step in path:
                table_data[current.y][current.x] = step.icon
                current = self._next_point(current, step)

        if self.start:
            table_data[self.start.y][self.start.x] = "S"

        if self.target:
            table_data[self.target.y][self.target.x] = "T"

        table = SingleTable(table_data[::-1])
        table.inner_row_border = True
        return table

    def __str__(self) -> str:
        return self.to_table().table
