import abc
import random
from typing import Tuple

from path_finder.chromosome import Chromosome
from path_finder.population import Population


class Selector(abc.ABC):
    def __init__(self, population: Population):
        self.population = population

    @abc.abstractmethod
    def select(self) -> Tuple[Chromosome, Chromosome]:
        raise NotImplementedError()


class RankingSelector(Selector):
    def select(self) -> Tuple[Chromosome, Chromosome]:
        rankings, items = zip(
            # start ranking from 1
            *enumerate(self.population.items, 1)
        )  # inverse of zip is zip
        return tuple(random.choices(items, weights=rankings[::-1], k=2))
