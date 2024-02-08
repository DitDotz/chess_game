from typing import Tuple, Dict
from pieces import *


def is_correct_format(notation: str) -> bool:
    """
    Check if the chess algebraic notation has the correct format.
    Valid notation format: <piece><origin><destination>
    """
    if len(notation) != 5:
        return False  # Notation length should be exactly 5 characters

    else:
        return True


def piece_exists_in_original_position(
    board: Dict[Tuple[int, int], Piece], notation: str
) -> bool:
    """
    Check if the piece specified in the notation exists in the original position on the board.
    """
    piece = notation[0]
    origin_row, origin_col = convert_to_coordinates(notation[1:3])
    color = Color.WHITE if notation[0].isupper() else Color.BLACK

    if (origin_row, origin_col) not in board:
        return False  # Original position is empty

    original_piece = board[(origin_row, origin_col)]

    if original_piece.type != FEN_MAP[piece.lower()] or original_piece.color != color:
        return False  # Piece at original position does not match the specified piece in the notation

    return True


def notation_is_valid(board: Dict[Tuple[int, int], Piece], notation: str) -> bool:
    """
    Check if the chess algebraic notation is valid.
    """
    return (
        is_correct_format(notation)
        and piece_exists_in_original_position(board, notation)
        # Add other validation checks as needed...
    )


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
