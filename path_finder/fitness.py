import abc
import math
from path_finder.chromosome import Chromosome
from path_finder.grid import Point, GridWrapper
from path_finder.utils import distance


class Fitness(abc.ABC):
    @abc.abstractmethod
    def __call__(self, chrom: Chromosome) -> float:
        raise NotImplementedError()


class NaiveFitness(Fitness):
    """
    Not great against walls
    """

    def __init__(self, grid: GridWrapper):
        self.grid = grid
        self.grid_size = grid.grid_x_size * grid.grid_y_size

    def __call__(self, chrom: Chromosome) -> float:
        return (
            self.grid_size
            - distance(self.grid.simulate_movement(chrom), self.grid.target)
            - (len(chrom) / self.grid_size)
        )


class PathFinderFitness(Fitness):
    def __init__(self, grid: GridWrapper):
        self.grid = grid
        self.grid_size = grid.grid_x_size * grid.grid_y_size

    def __call__(self, chrom: Chromosome) -> float:
        dist = distance(self.grid.simulate_movement(chrom), self.grid.target)
        if dist != 0:
            return self.grid_size - dist
        else:
            return self.grid_size - (len(chrom) / self.grid_size)
        # return (
        #     self.grid_size
        #     - distance(self.grid.simulate_movement(chrom), self.grid.target)
        #     - (len(chrom) / self.grid_size)
        # )


class PathFinderFitnessRewardLength(Fitness):
    def __init__(self, grid: GridWrapper):
        self.grid = grid
        self.grid_size = grid.grid_x_size * grid.grid_y_size

    def __call__(self, chrom: Chromosome) -> float:
        dist = distance(self.grid.simulate_movement(chrom), self.grid.target)
        # if dist == 1:
        #     # fix no motivation for last step (barrier not possible)
        #     return self.grid_size - dist
        if dist != 0:
            return self.grid_size - dist + min((len(chrom) / self.grid_size), 0.9999)
        else:
            # reward extra 1 for destination to make that beat length reward
            return self.grid_size + 1 - (len(chrom) / self.grid_size ** 2)
