"""
The population ued by the algorithm
"""
from typing import Sequence
from collections import namedtuple
from path_finder.chromosome import Chromosome
from path_finder.fitness import Fitness

RankedItem = namedtuple("RankedItem", "fitness chromosome")


class Population:
    """
    A population of chromosomes. replaced in each generation.
    """

    def __init__(self, items: Sequence[Chromosome], fitness_func: Fitness):
        """
        :param items: List of chromosomes to use as the population
        :param fitness_func: The fitness func to use for selection process
        """
        self.fitness_func = fitness_func
        self.population = sorted(
            (RankedItem(self.fitness_func(chrom), chrom) for chrom in items),
            key=lambda ranked_item: ranked_item.fitness,
            reverse=True,
        )
        self.population_length = len(self.population)
        self.median_index = self.population_length // 2

    @property
    def items(self) -> Sequence[Chromosome]:
        """
        :return: The chromosomes in the population
        """
        return [item.chromosome for item in self.population]

    @property
    def top_item(self) -> Chromosome:
        """
        :return: The chromosome with the highest fitness in the population
        """
        return self.population[0].chromosome

    @property
    def top_fitness(self) -> Chromosome:
        """
        :return: The fitness of the top chromosome
        """
        return self.population[0].fitness

    @property
    def median_item(self) -> Chromosome:
        """
        :return: The chromosome with the median fitness
        """
        return self.population[self.median_index].chromosome

    @property
    def median_fitness(self) -> Chromosome:
        """
        :return: The fitness of the median chromosome
        """
        return self.population[self.median_index].fitness
