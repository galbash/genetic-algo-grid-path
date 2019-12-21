"""
Selecting phase
"""
import abc
import random
from typing import Tuple, Iterable

from path_finder.chromosome import Chromosome
from path_finder.population import Population


class Selector(abc.ABC):
    """
    A selector, used for the selection phase.
    """

    def __init__(self, population: Population):
        """
        :param population: The population to choose from
        """
        self.population = population

    @abc.abstractmethod
    def select(self, count) -> Iterable[Tuple[Chromosome, Chromosome]]:
        """
        Selects items from the Selector's population
        :param count: Ampunt of items to select
        :return: A list of length `count` of pairs of items
        """
        raise NotImplementedError()


class RankingSelector(Selector):
    """
    A selector based on the ranking method
    """

    def select(self, count) -> Iterable[Tuple[Chromosome, Chromosome]]:
        """
        See Selector.select
        """
        rankings, items = zip(
            # start ranking from 1
            *enumerate(self.population.items, 1)
        )  # inverse of zip is zip
        return zip(
            random.choices(items, weights=rankings[::-1], k=count),
            random.choices(items, weights=rankings[::-1], k=count),
        )
