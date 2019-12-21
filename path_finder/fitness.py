"""
Various fitness functions to control the specimen selection in the reproduction stage
"""
import abc
from path_finder.chromosome import Chromosome
from path_finder.grid import GridWrapper
from path_finder.point import distance


class Fitness(abc.ABC):
    """
    A fitness function
    """

    def __init__(self, grid: GridWrapper):
        """
        :param grid: The environment we use
        """
        self.grid = grid
        self.grid_size = grid.grid_x_size * grid.grid_y_size

    @abc.abstractmethod
    def __call__(self, chrom: Chromosome) -> float:
        """
        :param chrom: The chromosome to calculate the fitness of
        :return: The fitness of the chromosome
        """
        raise NotImplementedError()


class NaiveFitness(Fitness):
    """
    A Naive fitness functions that converges fast when it hits a wall
    """

    def __call__(self, chrom: Chromosome) -> float:
        """
        see: Fitness.__call__
        """
        return (
            self.grid_size
            - distance(self.grid.simulate_movement(chrom), self.grid.target)
            - (len(chrom) / self.grid_size)
        )


class PathFinderFitness(Fitness):
    """
    A fitness function that only looks at chromosome length once we hit the target
    """

    def __call__(self, chrom: Chromosome) -> float:
        """
        see: Fitness.__call__
        """
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
    """
    A fitness function that rewards long chromosomes over short chromosomes which do
    not hit the target
    """

    def __call__(self, chrom: Chromosome) -> float:
        """
        see: Fitness.__call__
        """
        # if (len(chrom)) >= self.grid_size:
        #     return 0

        dist = distance(self.grid.simulate_movement(chrom), self.grid.target)
        # if dist == 1:
        #     # fix no motivation for last step (barrier not possible)
        #     return self.grid_size - dist
        if dist != 0:
            return self.grid_size - dist + min((len(chrom) / self.grid_size), 0.9999)
        else:
            # reward extra 1 for destination to make that beat length reward
            return self.grid_size + 1 - (len(chrom) / self.grid_size)
