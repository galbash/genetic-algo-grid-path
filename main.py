"""
An interface to run the path finder genetic algorithm
"""
from typing import Callable
import os.path
import itertools
import logging
import progressbar
import fire

from path_finder.finder import Finder
from path_finder.point import distance
from path_finder.environments import *
from path_finder.fitness import (
    PathFinderFitnessRewardLength,
    PathFinderFitnessRewardLengthDistanceGroups,
)
from path_finder.reporter import Reporter

logging.getLogger().setLevel(logging.INFO)

POPULATION_SIZES = [20, 40, 60]


def run_for_env(
    name: str,
    creator: Callable[[int], GridWrapper],
    grid_size: Size,
    population_size: int,
) -> None:
    """
    Executes the genetic algorithm for a specific setting
    :param name: name for the execution
    :param creator: environment creator function
    :param grid_size: the grid size to use
    :param population_size: the population size to use
    """
    logging.info("starting execution for %s", name)
    grid = creator(grid_size)
    finder = Finder(grid, population_size, PathFinderFitnessRewardLengthDistanceGroups)
    top_score = 0
    no_change_count = 0
    with Reporter(
        finder, os.path.join("out", name)
    ) as reporter, progressbar.ProgressBar(max_value=progressbar.UnknownLength) as bar:
        dist = grid.calculate_distance(finder.population.top_item)
        while (
            dist != 0
            or len(finder.population.top_item) > distance(grid.start, grid.target)
        ) and no_change_count < 1500:
            reporter.report()
            finder.run_generation()
            bar.update(finder.generation)

            if finder.population.top_fitness > top_score:
                no_change_count = 0
                top_score = finder.population.top_fitness
                print(grid.to_table(finder.population.top_item).table)
                logging.info("new top fitness. distance from target: %d", dist)
            else:
                no_change_count += 1

            if finder.population.top_fitness < top_score:
                top_score = finder.population.top_fitness
                print(grid.to_table(finder.population.top_item).table)
                logging.info("we lost our top score. current dist: %d", dist)

            dist = grid.calculate_distance(finder.population.top_item)

        reporter.report()
    logging.info("execution for %s done", name)


def main(env_name: str = None, pop_size: int = None, size: str = None):
    """
    interface for running the algorithm
    :param env_name: specific environment to use. defaults to all
    :param pop_size: specific population size to use. defaults to all
    :param size: specific grid size to use. defaults to all
    """
    env_items = ENVS.items()
    env_names = [env_name] if env_name else [env[0] for env in env_items]
    env_creators = [ENVS[env_name]] if env_name else [env[1] for env in env_items]
    pop_sizes = [pop_size] if pop_size else POPULATION_SIZES
    sizes = [Size[size]] if size else list(Size)
    for (env_name, env), pop_size, grid_size in itertools.product(
        zip(env_names, env_creators), pop_sizes, sizes
    ):
        run_for_env(f"{env_name}-{grid_size.name}-{pop_size}", env, grid_size, pop_size)


if __name__ == "__main__":
    fire.Fire(main)
