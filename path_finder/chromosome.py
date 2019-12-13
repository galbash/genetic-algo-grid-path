"""
A chromosome
"""

import enum
import typing


@enum.unique
class Direction(enum.Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


Chromosome = typing.Sequence[Direction]
