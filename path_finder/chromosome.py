"""
A chromosome
"""

import typing
import random

from path_finder.direction import Direction, DIRECTIONS

Chromosome = typing.Sequence[Direction]


def random_chromosome(size: int):
    return random.choices(DIRECTIONS, k=size)
