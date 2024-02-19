import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notation import Notation
from board import Board
from pieces import Piece, Color, PieceType


# is_correct_format
def test_is_correct_format_correct():
    sample_notation = "pa2a4"
    assert Notation.is_correct_format(sample_notation) == True


def test_is_correct_format_incorrect_length():
    sample_notation = "ka2a42"
    assert Notation.is_correct_format(sample_notation) == False


def test_is_correct_format_incorrect_piece():
    sample_notation = "ia2a4"
    assert Notation.is_correct_format(sample_notation) == False


def test_is_correct_format_incorrect_col_letter():
    sample_notation = "kj2a4"
    assert Notation.is_correct_format(sample_notation) == False


def test_is_correct_format_incorrect_row_number():
    sample_notation = "kj2a0"
    assert Notation.is_correct_format(sample_notation) == False


# piece_exists_in_original_position


def test_piece_exists_in_original_position_valid():
    board = {(1, 0): Piece(x=1, y=2, type=PieceType.PAWN, color=Color.BLACK)}
    notation = "pa7a6"
    assert Notation.piece_exists_in_original_position(board, notation) == True


def test_piece_exists_in_original_position_invalid_final_pos():
    board = {
        (1, 0): Piece(x=1, y=0, type=PieceType.PAWN, color=Color.BLACK),
        (1, 1): Piece(x=1, y=1, type=PieceType.ROOK, color=Color.BLACK),
    }
    notation = "pa7b5"
    assert Notation.piece_exists_in_original_position(board, notation) == True


def test_piece_exists_in_original_position_invalid_color():
    board = {(1, 0): Piece(x=1, y=0, type=PieceType.PAWN, color=Color.BLACK)}
    notation = "Pa7a6"
    assert Notation.piece_exists_in_original_position(board, notation) == False


def test_interpret_notation_valid():
    notation = "pa7a6"
    expected_result = [(1, 0), Piece(x=2, y=0, type=PieceType.PAWN, color=Color.BLACK)]
    assert Notation.interpret_notation(notation) == expected_result


def test_convert_to_coordinates():
    assert Notation.convert_to_coordinates("a2") == (6, 0)
    assert Notation.convert_to_coordinates("h7") == (1, 7)


def test_notation_is_valid_all_valid():
    # Create a board with some pieces for testing
    board = {(1, 0): Piece(x=1, y=0, type=PieceType.PAWN, color=Color.BLACK)}
    # Assume the board is set up with some pieces in the initial positions

    # Provide a valid notation for testing
    notation = "pa7a6"
    assert Notation.notation_is_valid(board, notation) == True


# Current implementation returns true because parsing a valid move requires the current state of the board
def test_notation_is_valid_invalid_final_pos():
    # Create a board with some pieces for testing
    board = {(1, 0): Piece(x=1, y=0, type=PieceType.PAWN, color=Color.BLACK)}
    # Assume the board is set up with some pieces in the initial positions

    # Provide a valid notation for testing
    notation = "pa7a3"
    assert Notation.notation_is_valid(board, notation) == False


def test_notation_is_valid_invalid_format():
    board = {(1, 0): Piece(x=1, y=0, type=PieceType.PAWN, color=Color.BLACK)}
    assert Notation.notation_is_valid(board, "pa2a42") == False  # Incorrect length


def test_notation_is_valid_piece_not_exist():
    board = {(1, 0): Piece(x=1, y=0, type=PieceType.PAWN, color=Color.BLACK)}
    # Test with notations where the specified piece does not exist at the original position
    assert Notation.notation_is_valid(board, "Pa7a6") == False  # No pawn at a5
