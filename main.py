from path_finder.finder import Finder
from path_finder.grid import Cell, Point, simulate_movement
from path_finder.utils import distance

GRID = [[Cell() for i in range(100)] for j in range(100)]

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

for i in range(28):
    GRID[60][i].blocked = True

for i, row in enumerate(GRID[::-1]):
    for j, cell in enumerate(row):
        print('*' if cell.blocked else ' ', end='')
    print()

input('>>>>>>')

START = Point(0, 0)
TARGET = Point(0, 99)
FINDER = Finder(GRID, START, TARGET, 40)


def main():
    while (
        simulate_movement(GRID, START, FINDER.population.top_item) != TARGET
        or len(FINDER.population.top_item) > distance(START, TARGET)
    ):
        #print("generation", FINDER.generation, "top", FINDER.population.top_item)
        print("generation", FINDER.generation)
        print("fitness", FINDER.population.population[0].fitness, "length", len(FINDER.population.top_item))
        print("min distance", distance(START, TARGET), "distance", distance(simulate_movement(GRID, START, FINDER.population.top_item), TARGET))
        FINDER.run_generation()

    print("done, chrom length:", len(FINDER.population.top_item))


if __name__ == "__main__":
    main()
