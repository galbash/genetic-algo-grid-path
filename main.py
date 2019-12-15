from typing import Callable
import os.path
import itertools
import logging
import progressbar

from path_finder.finder import Finder
from path_finder.point import distance
from path_finder.environments import *
from path_finder.fitness import PathFinderFitnessRewardLength
from path_finder.reporter import Reporter

logging.getLogger().setLevel(logging.INFO)


ENVS = [
    empty_env,
    center_block_env,
    peekhole_env,
    wall_env,
    multi_wall_env,
    multiway_wall_env,
]
POPULATION_SIZES = [20, 40, 60]


def run_for_env(
    name: str,
    creator: Callable[[int], GridWrapper],
    grid_size: Size,
    population_size: int,
):
    logging.info("starting execution for %s", name)
    grid = creator(grid_size)
    finder = Finder(grid, population_size, PathFinderFitnessRewardLength)
    top_score = 0
    no_change_count = 0
    with Reporter(
        finder, os.path.join("out", name)
    ) as reporter, progressbar.ProgressBar(max_value=progressbar.UnknownLength) as bar:
        while (
            grid.calculate_distance(finder.population.top_item) != 0
            or len(finder.population.top_item) > distance(grid.start, grid.target)
        ) and no_change_count < 2000:
            reporter.report()
            finder.run_generation()
            bar.update(finder.generation)

            if finder.population.top_fitness > top_score:
                no_change_count = 0
                top_score = finder.population.top_fitness
            else:
                no_change_count += 1

        reporter.report()
    logging.info("execution for %s done", name)


def main():
    for env, pop_size, grid_size in itertools.product(
        ENVS, POPULATION_SIZES, list(Size)
    ):
        run_for_env(
            f"{env.__name__}-{grid_size.name}-{pop_size}", env, grid_size, pop_size
        )


if __name__ == "__main__":
    main()
