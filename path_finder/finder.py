"""
The path finder, used to run the genetic algorithm
"""
import copy
from typing import Type
from path_finder.grid import GridWrapper
from path_finder.operators import (
    PathFinderChoose,
    PathFinderCross,
    AddMutation,
    SwitchMutation,
    RemoveMutation,
    RemovePairMutation,
    PathFinderOperationSequence,
)

from path_finder.fitness import Fitness
from path_finder.chromosome import random_chromosome
from path_finder.point import distance
from path_finder.population import Population
from path_finder.selector import RankingSelector


class Finder:
    """
    The path finder, used to run the genetic algorithm
    """

    ELITISM_FACTOR = 0.05

    def __init__(
        self, grid: GridWrapper, population_size: int, fitness_class: Type[Fitness]
    ):
        """
        :param grid: The environment to run the algorithm on
        :param population_size: The size of the population to generate
        :param fitness_class: The fitness function to use
        """
        self.grid = grid
        self.min_dist = distance(grid.start, grid.target)
        self.operations = PathFinderOperationSequence(
            PathFinderCross(),
            PathFinderChoose(),
            [
                SwitchMutation(self.min_dist),
                AddMutation(self.min_dist),
                RemoveMutation(self.min_dist),
                RemovePairMutation(self.min_dist),
            ],
        )
        self.population_size = population_size
        self.fitness_func = fitness_class(grid)
        self.population = Population(
            [random_chromosome(self.min_dist) for _ in range(self.population_size)]
            + [
                random_chromosome(self.min_dist * 2)
                for _ in range(self.population_size)
            ],
            self.fitness_func,
        )
        self.generation = 0

    def run_generation(self) -> None:
        """
        makes an iteration: mates parents and creates a new generation of children
        """
        new_items = []

        # elitism
        while len(new_items) < self.population_size * self.ELITISM_FACTOR:
            new_items.append(copy.deepcopy(self.population.top_item))

        remaining_count = self.population_size - len(new_items)
        selector = RankingSelector(self.population)
        couples = selector.select(remaining_count)
        for parent1, parent2 in couples:
            new_item = self.operations(parent1, parent2)
            new_items.append(new_item)

        self.population = Population(new_items, self.fitness_func)
        self.generation += 1
