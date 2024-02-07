from typing import Tuple, Dict
from pieces import *


def interpret_notation(notation: str) -> Piece:
    """
    Interpret chess algebraic notation and return the piece type, color, x, and y coordinates.
    """
    # Extract the piece type, color, and destination coordinates from the notation
    piece_type: PieceType = PieceType.EMPTY
    color: Color = Color.NONE
    x, y = None, None

    # Handle notation with length 3
    if len(notation) == 3:
        piece_type = (
            PieceType.PAWN
        )  # By default, if only coordinates are given, it's a pawn move

        if notation[0].lower() in FEN_MAP:
            piece_type = FEN_MAP[notation[0].lower()]
        x = ord(notation[1]) - ord("a")
        y = 8 - int(notation[2])

    # Handle notation with length 4 (captures or disambiguated moves)
    elif len(notation) == 4:
        piece_type = FEN_MAP[notation[0].lower()]
        x = ord(notation[2]) - ord("a")
        y = 8 - int(notation[3])

    color = Color.WHITE if notation[0].isupper() else Color.BLACK
    piece = Piece(x=x, y=y, color=color, type=piece_type)

    return piece


class ChessNotationConverter:
    @staticmethod
    def convert_to_coordinates(chess_notation: str) -> Tuple[int, int]:
        """
        Convert algebraic chess notation to grid coordinates.
        """
        column_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        if len(chess_notation) != 2:
            raise ValueError("Invalid chess notation format")

        file_char, rank_char = chess_notation[0], chess_notation[1]
        if file_char not in column_map or not rank_char.isdigit():
            raise ValueError("Invalid chess notation format")

        # Convert rank to 0-indexed row, and adjust for Python indexing
        row = 8 - int(rank_char)
        column = column_map[file_char]

        return row, column


# Example usage:
notation = "c1"
row, column = ChessNotationConverter.convert_to_coordinates(notation)
print(f"Chess notation '{notation}' corresponds to grid position: ({row}, {column})")
