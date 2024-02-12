from typing import Dict, Tuple

import pytest
import os
import sys
from moves import UniversalMovementValidation
from pieces import Piece, PieceType, Color
from board import Board
from notation import interpret_notation

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_is_within_board_true():
    # Test cases for points within the board
    assert UniversalMovementValidation.is_within_board(0, 0) == True
    assert UniversalMovementValidation.is_within_board(3, 3) == True
    assert UniversalMovementValidation.is_within_board(7, 7) == True


def test_is_within_board_false():
    # Test cases for points outside the board
    assert UniversalMovementValidation.is_within_board(-1, 0) == False
    assert UniversalMovementValidation.is_within_board(8, 3) == False
    assert UniversalMovementValidation.is_within_board(7, 8) == False


def test_is_not_occupied_by_allies():
    # Create a sample board
    board: Dict[Tuple[int, int], Piece] = {
        (0, 0): Piece(0, 0, type=PieceType.ROOK, color=Color.WHITE),
        (1, 1): Piece(1, 1, type=PieceType.EMPTY, color=Color.NONE),
        (2, 2): Piece(2, 2, type=PieceType.PAWN, color=Color.BLACK),
    }

    # Test cases for new positions not occupied by allies
    test_color = Color.WHITE

    assert (
        UniversalMovementValidation.is_not_occupied_by_allies(board, 1, 1, test_color)
        == True
    )
    assert (
        UniversalMovementValidation.is_not_occupied_by_allies(board, 2, 2, test_color)
        == True
    )

    assert (
        UniversalMovementValidation.is_not_occupied_by_allies(board, 0, 0, test_color)
        == False
    )


def test_is_occupied_by_opposing():
    # Create a sample board
    board = {
        (1, 1): Piece(1, 1, type=PieceType.EMPTY, color=Color.NONE),
        (2, 2): Piece(2, 2, type=PieceType.PAWN, color=Color.BLACK),
        (0, 0): Piece(0, 0, type=PieceType.ROOK, color=Color.WHITE),
    }

    test_color = Color.BLACK

    assert (
        UniversalMovementValidation.is_occupied_by_opposing(board, 0, 0, test_color)
        == True
    )

    assert (
        UniversalMovementValidation.is_occupied_by_opposing(board, 1, 1, test_color)
        == False
    )

    assert (
        UniversalMovementValidation.is_occupied_by_opposing(board, 2, 2, test_color)
        == False
    )


def test_is_pinned_to_own_king():
    # piece will be moved arbitrarily without consideration of valid moves
    # this means it will likely break once valid moves are incorporated
    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"

    board = Board()
    board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
    origin_pos, final_pos_piece = interpret_notation("Rd4d1")
    piece_to_move = board.board[origin_pos]
    print(board)

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            piece=piece_to_move,
            board=board.board,
            new_x=final_pos_piece.x,
            new_y=final_pos_piece.y,
        )
        == True
    )

    # movements to test
    # origin_pos, final_pos_piece = interpret_notation("Rd4d1") == True
    # origin_pos, final_pos_piece = interpret_notation("Re4e6") == True
    # origin_pos, final_pos_piece = interpret_notation("Rf4f1") == True
    # origin_pos, final_pos_piece = interpret_notation("Re2a2") == False
