import abc
from path_finder.chromosome import Chromosome
from path_finder.grid import Point, simulate_movement, Grid
from path_finder.utils import distance


class Fitness(abc.ABC):
    @abc.abstractmethod
    def __call__(self, chrom: Chromosome) -> float:
        raise NotImplementedError()


class PathFinderFitness(Fitness):
    def __init__(self, grid: Grid, start: Point, target: Point):
        self.grid = grid
        self.grid_x_size = len(grid[0])
        self.grid_y_size = len(grid)
        self.start = start
        self.target = target
        self.grid_size = self.grid_x_size * self.grid_y_size

    def __call__(self, chrom: Chromosome) -> float:
        return (
            self.grid_size
            - distance(simulate_movement(self.grid, self.start, chrom), self.target)
            - (len(chrom) / self.grid_size)
        )
