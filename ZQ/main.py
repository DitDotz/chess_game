from enum import Enum
from dataclasses import dataclass

Grid = "dict[Position, Piece]"


# Initialize a grid filled with pieces
# data structure is a dictionary of a tuple of integers as the key
# and a Piece Class as the value


def empty_board() -> Grid:
    grid: Grid = {}  # empty dictionary
    for x in range(8):
        for y in range(8):
            grid[(x, y)] = Piece(x, y)  # key of the dictionary is a tuple of ints
    return grid


class Color(Enum):
    WHITE = 0
    BLACK = 1
    NONE = -1


@dataclass
class Piece:
    x: int
    y: int
    color: Color = Color.NONE


grid = empty_board()
print(grid)
