from path_finder.grid import Cell

SMALL_SIZE = 10
LARGE_SIZE = 100


def _create_env(size):
    return [[Cell() for _ in range(size)] for _ in range(size)]


def small_empty():
    return _create_env(SMALL_SIZE)


def large_empty():
    return _create_env(LARGE_SIZE)


def small_minor_block():
    grid = small_empty()
