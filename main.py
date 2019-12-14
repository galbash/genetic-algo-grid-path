from path_finder.finder import Finder
from path_finder.utils import distance
from path_finder.environments import *
from path_finder.fitness import PathFinderFitnessRewardLength


# for i in range(100):
#     if i % 25 != 0:
#         GRID[50][i].blocked = True
#
# for i in range(99):
#     if i != 30:
#         GRID[i][60].blocked = True
#
# GRID[99][62].blocked = True

# for i in range(40, 100, 4):
#     if i % 8 == 0:
#         for j in range(0, 54):
#             GRID[i][j].blocked = True
#     else:
#         for j in range(49, 100):
#             GRID[i][j].blocked = True

# for i in range(28):
#     GRID[60][i].blocked = True



def main():
    grid = wall_env(Size.SMALL)
    print(grid)
    finder = Finder(grid, 50, PathFinderFitnessRewardLength)
    input('start >>>>>>>')
    top_score = 0
    no_change_count = 0
    while (
            (grid.simulate_movement(finder.population.top_item) != grid.target
        or len(finder.population.top_item) > distance(grid.start, grid.target)) and no_change_count < 2000

    ):
        current_best_fit = finder.population.population[0].fitness
        print("generation", finder.generation)
        print("fitness", current_best_fit, "length", len(finder.population.top_item))
        print("min distance", distance(grid.start, grid.target), "distance", distance(grid.simulate_movement(finder.population.top_item), grid.target))
        finder.run_generation()

        if current_best_fit > top_score:
            no_change_count = 0
            top_score = current_best_fit
        else:
            no_change_count += 1


    print("done, chrom length:", len(finder.population.top_item), "no_change_count:", no_change_count)
    print(grid.to_table(finder.population.top_item).table)


if __name__ == "__main__":
    main()
