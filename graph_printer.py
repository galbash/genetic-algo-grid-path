"""
analyze mtrics in a graphic way
"""
import logging
import os.path
import itertools
import matplotlib.pyplot as plt
from path_finder.environments import ENVS, Size
from main import POPULATION_SIZES
from path_finder.reporter import Reader

logging.getLogger().setLevel(logging.INFO)

import numpy

exp = lambda x: 10 ** x
log_func = lambda y: numpy.log(y)


class GraphCreator:
    """
    Creates Graphs from algorithm execution results
    """

    def __init__(self, base_path, env_name, grid_size: Size):
        """
        :param base_path: Path of the results
        :param env_name: The environment we are analyzing
        :param grid_size: The grid size we are analyzing
        """
        self.base_path = base_path
        self.env_name = env_name
        self.grid_size = grid_size
        self.output_path = os.path.join(base_path, "graphs")
        os.makedirs(self.output_path, exist_ok=True)

    def create_graph(self):
        """
        paints the graphs
        """
        logging.info(f"starting {self.env_name} {self.grid_size.name}")
        population_stats = {
            pop_size: list(
                Reader(
                    os.path.join(
                        self.base_path,
                        f"{self.env_name}-{self.grid_size.name}-{pop_size}",
                    )
                ).read()
            )
            for pop_size in POPULATION_SIZES
        }
        max_generation = max(len(pop) for pop in population_stats.values())
        self.save_graph(
            population_stats, max_generation, "length", "Path Length (Cells)",
        )
        self.save_graph(
            population_stats,
            max_generation,
            "distance",
            "Distance from target (Cells)",
        )
        self.save_graph(population_stats, max_generation, "fitness")
        logging.info("done")

    def save_graph(
        self, population_stats, max_generation, stat_name, y_title=None,
    ) -> None:
        logging.info(f"generating stat {stat_name}")
        y_title = y_title if y_title else stat_name.capitalize()
        fig, axs = plt.subplots(
            2, num=None, figsize=(14, 12), dpi=80, facecolor="w", edgecolor="k"
        )
        plt.xlabel("Generation")
        for i, stat_type in enumerate(("top", "median",)):
            ax = axs[i]
            for pop_size, stats in population_stats.items():
                self.add_plot(
                    f"{stat_type}_{stat_name}", stats, max_generation, pop_size, ax
                )
            ax.set_ylabel(y_title)
            ax.legend(loc="best")

        fig.savefig(
            os.path.join(
                self.output_path, f"{self.env_name}-{self.grid_size.name}-{stat_name}",
            )
        )
        plt.close(fig)
        plt.clf()

    def add_plot(self, stat_type, stats, max_generation, pop_size, ax) -> None:
        sampling = 1
        dots = [
            getattr(stat, stat_type)
            for i, stat in enumerate(stats)
            if i % sampling == 0
        ]
        logging.debug(f"got {len(dots)} dots")
        ax.plot(
            range(1, max_generation + 2, sampling)[: len(dots)],
            dots,
            label=f"{stat_type}: {pop_size}",
        )


def main():
    """
    Generates graphs from algorithm metrics data
    """
    for (env_name, env), grid_size in itertools.product(ENVS.items(), list(Size)):
        GraphCreator("out", env_name, grid_size).create_graph()


if __name__ == "__main__":
    main()
