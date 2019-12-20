import math
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
    def __init__(self, base_path, env_name, grid_size: Size):
        self.base_path = base_path
        self.env_name = env_name
        self.grid_size = grid_size
        self.output_path = os.path.join(base_path, "graphs")
        os.makedirs(self.output_path, exist_ok=True)

    def create_graph(self):
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
            population_stats,
            max_generation,
            "length",
            "Path Length (Cells)",
        )
        self.save_graph(
            population_stats,
            max_generation,
            "distance",
            "Distance from target (Cells)",
        )
        self.save_graph(
            population_stats, max_generation, "fitness"
        )
        logging.info("done")

    def save_graph(
        self,
        population_stats,
        max_generation,
        stat_name,
        y_title=None,
        scale="symlog",
        **scale_kargs,
    ) -> None:
        logging.info(f"generating stat {stat_name}")
        y_title = y_title if y_title else stat_name.capitalize()
        fig, axs = plt.subplots(len(population_stats),
            num=None, figsize=(14, 12), dpi=80, facecolor="w", edgecolor="k"
        )
        plt.xlabel("Generation")
        for i, (pop_size, stats) in enumerate(population_stats.items()):
            self.add_plot(f"median_{stat_name}", stats, max_generation, pop_size,axs[i])
        for i, (pop_size, stats) in enumerate(population_stats.items()):
            ax = axs[i]
            self.add_plot(f"top_{stat_name}", stats, max_generation, pop_size, axs[i])
            #ax.title(f"{stat_name} by generation. population: {pop_size}")
            ax.set_ylabel(y_title)
            ax.legend(loc="best")
            ax.set_yscale(scale, **scale_kargs)

        fig.savefig(
            os.path.join(
                self.output_path,
                f"{self.env_name}-{self.grid_size.name}-{stat_name}",
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
        if stat_type.endswith("fitness"):
            dots = [dot / ((self.grid_size.value ** 2) + 1) for dot in dots]
        # logging.info("%s", dots)
        logging.debug(f"got {len(dots)} dots")
        ax.plot(
            range(1, max_generation + 2, sampling)[: len(dots)],
            dots,
            label=f"{stat_type}: {pop_size}",
        )


def main():
    for env, grid_size in itertools.product(ENVS, list(Size)):
        GraphCreator("out", env.__name__, grid_size).create_graph()


if __name__ == "__main__":
    main()
