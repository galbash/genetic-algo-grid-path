from typing import Sequence


class Cell:
    def __init__(self, blocked):
        self.blocked = blocked


Grid = Sequence[Sequence[Cell]]
