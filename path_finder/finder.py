import copy
from path_finder.grid import GridWrapper
from path_finder.operators import (
    PathFinderChoose,
    PathFinderCross,
    AddMutation,
    SwitchMutation,
    RemoveMutation,
    PathFinderOperationSequence,
)

from path_finder.chromosome import random_chromosome
from path_finder.utils import distance
from path_finder.fitness import PathFinderFitness
from path_finder.population import Population
from path_finder.selector import RankingSelector


class Finder:
    ELITISM_FACTOR = 0.05

    def __init__(
        self, grid: GridWrapper, population_size: int, fitness_class=PathFinderFitness
    ):
        self.grid = grid
        self.min_dist = distance(grid.start, grid.target)
        self.operations = PathFinderOperationSequence(
            PathFinderCross(),
            PathFinderChoose(),
            [
                SwitchMutation(self.min_dist),
                AddMutation(self.min_dist),
                RemoveMutation(self.min_dist),
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
        new_items = []

        # elitism
        while len(new_items) < self.population_size * self.ELITISM_FACTOR:
            new_items.append(copy.deepcopy(self.population.top_item))

        selector = RankingSelector(self.population)
        while len(new_items) < self.population_size:
            new_item = self.operations(*selector.select())
            new_items.append(new_item)

        self.population = Population(new_items, self.fitness_func)
        self.generation += 1
