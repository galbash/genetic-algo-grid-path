import csv
import os
import os.path
from dataclasses import dataclass, asdict
from path_finder.finder import Finder


@dataclass
class FinderState:
    generation: int
    top_distance: int
    top_length: int
    top_fitness: float
    median_distance: int
    median_length: int
    median_fitness: float


FIELD_NAMES = list(FinderState.__annotations__.keys())


class Reporter:
    def __init__(self, finder: Finder, path: str, print_stats: bool = False):
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
