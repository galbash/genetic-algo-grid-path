from path_finder.grid import Grid
from path_finder.operators import (
    PathFinderChoose,
    PathFinderCross,
    AddMutation,
    SwitchMutation,
    RemoveMutation,
    PathFinderOperationSequence,
)


class Finder:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.sequence = PathFinderOperationSequence(
            PathFinderCross,
            PathFinderChoose,
            [SwitchMutation, AddMutation, RemoveMutation],
        )
