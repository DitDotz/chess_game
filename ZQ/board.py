from typing import Dict, Tuple
from pieces import *


class Board:
    def __init__(self) -> None:
        self.board = self.empty_board()

    def empty_board(self) -> Dict[Tuple[int, int], Piece]:
        board: Dict[Tuple[int, int], Piece] = {}
        for x in range(8):
            for y in range(8):
                board[(x, y)] = Piece(x, y)
        return board

    def process_fen(self, fen: str) -> Dict[Tuple[int, int], Piece]:
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

        for x in range(x, 8):
            for y in range(y, 8):
                if (x, y) not in position_map:
                    position_map[(x, y)] = Piece(x, y)

        for position, fen_char in position_map.items():
            x, y = position
            piece = Piece(
                x,
                y,
                type=PieceType(FEN_MAP[fen_char.lower()]),
                color=Color.WHITE if fen_char.isupper() else Color.BLACK,
            )
            self.board[position] = piece

        return self.board

    def __repr__(self) -> str:
        representation = ""
        for x in range(8):
            if x != 0:
                representation += (
                    "|---" * 8 + "|\n"
                )  # Add horizontal lines between rows

            for y in range(8):
                piece = self.board[(x, y)]
                representation += (
                    f"| {piece.repr} "  # Add vertical lines between columns
                )
            representation += "\n"

        return representation
