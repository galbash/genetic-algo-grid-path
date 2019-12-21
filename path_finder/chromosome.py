"""
A chromosome used by the genetic algorithm
"""

import typing
import random

from path_finder.direction import Direction, DIRECTIONS

Chromosome = typing.Sequence[Direction]


def random_chromosome(size: int):
    """
    :param size: the length for the chromosome to build
    :return: a randomly built chromosome
    """
    return random.choices(DIRECTIONS, k=size)
