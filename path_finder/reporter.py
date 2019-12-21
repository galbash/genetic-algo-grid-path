"""
Metrics collection
"""
import os
import os.path
import csv
from typing import Iterator
from dataclasses import dataclass, asdict
from dataclass_csv import DataclassReader
from path_finder.finder import Finder


@dataclass
class FinderState:
    """
    A state of the algorithm in a given generation
    """

    generation: int
    top_distance: int
    top_length: int
    top_fitness: float
    median_distance: int
    median_length: int
    median_fitness: float


FIELD_NAMES = list(FinderState.__annotations__.keys())


class Reporter:
    """
    A class used for metrics collection
    """

    def __init__(self, finder: Finder, path: str, print_stats: bool = False):
        """
        :param finder: The finder we are tracking
        :param path: The disk path to store metrics in
        :param print_stats: debug flag, if true stats will be printed to output
        """
        self.finder = finder
        self.path = path
        self.stats = None
        self.print_stats = print_stats

    def __enter__(self):
        self.stats = []
        os.makedirs(self.path, exist_ok=True)
        with open(os.path.join(self.path, "initial_grid.txt"), "wt") as f:
            f.write(str(self.finder.grid))

        return self

    def report(self) -> None:
        """
        Store metrics on current generation
        """
        top_item = self.finder.population.top_item
        median_item = self.finder.population.median_item
        stat = FinderState(
            self.finder.generation,
            self.finder.grid.calculate_distance(top_item),
            len(top_item),
            self.finder.population.top_fitness,
            self.finder.grid.calculate_distance(median_item),
            len(median_item),
            self.finder.population.median_fitness,
        )
        if self.print_stats:
            print(stat)
        self.stats.append(stat)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(os.path.join(self.path, "report.csv"), "wt") as f:
            writer = csv.DictWriter(f, FIELD_NAMES)
            writer.writeheader()
            writer.writerows([asdict(stat) for stat in self.stats])

        with open(os.path.join(self.path, "final_grid.txt"), "wt") as f:
            f.write(
                self.finder.grid.to_table(self.finder.population.top_item).table + "\n"
            )

        # not deleting stats cause can be used after exit


class Reader:
    """
    A class used to read Reporter metrics
    """

    def __init__(self, path):
        """
        :param path: the disk path metrics are stored in
        """
        self.path = path

    def read(self) -> Iterator[FinderState]:
        """
        Reads the Reporter's metrics
        :return: A list of states the algorithm execution reported
        """
        with open(os.path.join(self.path, "report.csv"), "rt") as f:
            reader = DataclassReader(f, FinderState)
            yield from reader
