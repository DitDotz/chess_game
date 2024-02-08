from typing import Tuple, Dict
from pieces import *


def interpret_notation(notation: str) -> List:
    """
    Interpret chess algebraic notation and return the piece type, color, x, and y coordinates.
    """
    # Extract the piece type, color, and destination coordinates from the notation

    piece_type = FEN_MAP[(notation[0].lower())]
    piece_color = Color.WHITE if notation[0].isupper() else Color.BLACK
    original_pos = convert_to_coordinates(notation[1:3])
    final_pos = convert_to_coordinates(notation[3:5])
    final_pos_piece = Piece(
        x=final_pos[0], y=final_pos[1], type=piece_type, color=piece_color
    )

    return [original_pos, final_pos_piece]


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
