from typing import Dict, Tuple
from pieces import *

Position = Tuple[int, int]
Grid = Dict[Position, Piece]


class Board:
    def __init__(self) -> None:
        self.board = self.empty_board()

    def empty_board(self) -> Grid:
        grid: Grid = {}  # empty dictionary
        for x in range(8):
            for y in range(8):
                grid[(x, y)] = Piece(x, y)  # key of the dictionary is a tuple of ints
        return grid

    @staticmethod
    def process_fen(fen: str) -> Dict[Position, str]:
        """
        Process the FEN string and return a dictionary containing the piece positions.
        """

        position_map: Dict[Tuple[int, int], str] = {}

        x, y = 0, 0

        for char in fen:
            if char == "/":
                x += 1
                y = 0
            elif char.isdigit():
                y += int(char)
            else:
                position_map[(x, y)] = char
                y += 1

        return position_map

    def map_pieces_to_board(self, pieces: List[Piece]) -> None:
        for piece in pieces:
            self.board[(piece.x, piece.y)] = piece
