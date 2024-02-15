from typing import Dict, Tuple

# import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from moves import UniversalMovementValidation, RookMovement
from pieces import Piece, PieceType, Color
from board import Board
from notation import interpret_notation


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


def test_is_pinned_to_own_king_diagonal_queen_pin():
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


def test_is_pinned_to_own_king_diagonal_bishop_pin():
    # piece will be moved arbitrarily without consideration of valid moves
    # this means it will likely break once valid moves are incorporated
    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"

    board = Board()
    print(board)
    board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
    origin_pos, final_pos_piece = interpret_notation("Rf4f1")
    piece_to_move = board.board[origin_pos]

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            piece=piece_to_move,
            board=board.board,
            new_x=final_pos_piece.x,
            new_y=final_pos_piece.y,
        )
        == True
    )


def test_is_pinned_to_own_king_can_move_along_x_ray_direction():
    # piece will be moved arbitrarily without consideration of valid moves
    # this means it will likely break once valid moves are incorporated
    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"

    board = Board()
    print(board)
    board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
    origin_pos, final_pos_piece = interpret_notation("Re4e6")
    piece_to_move = board.board[origin_pos]

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            piece=piece_to_move,
            board=board.board,
            new_x=final_pos_piece.x,
            new_y=final_pos_piece.y,
        )
        == False
    )


def test_is_pinned_to_own_king_knight_not_involved():
    # piece will be moved arbitrarily without consideration of valid moves
    # this means it will likely break once valid moves are incorporated
    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"

    board = Board()
    print(board)
    board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
    origin_pos, final_pos_piece = interpret_notation("Re2a2")
    piece_to_move = board.board[origin_pos]

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            piece=piece_to_move,
            board=board.board,
            new_x=final_pos_piece.x,
            new_y=final_pos_piece.y,
        )
        == False
    )


# Test RookMovement
def test_RookMovement_valid_moves_along_x_ray_direction():

    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = interpret_notation("Re4e6")
    rook = board.board[origin_pos]
    rook_movement = RookMovement(rook)
    valid_moves = rook_movement.get_valid_moves(
        board.board, final_pos_piece.x, final_pos_piece.y
    )

    expected_moves = [(3, 4), (2, 4), (1, 4), (0, 4)]
    assert valid_moves == expected_moves


def test_RookMovement_valid_moves_pinned():

    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = interpret_notation("Rd4d5")
    rook = board.board[origin_pos]
    rook_movement = RookMovement(rook)
    valid_moves = rook_movement.get_valid_moves(
        board.board, final_pos_piece.x, final_pos_piece.y
    )

    expected_moves = []
    assert valid_moves == expected_moves


def test_RookMovement_valid_moves_capture():

    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = interpret_notation("Re2e1")
    rook = board.board[origin_pos]
    rook_movement = RookMovement(rook)
    valid_moves = rook_movement.get_valid_moves(
        board.board, final_pos_piece.x, final_pos_piece.y
    )

    expected_moves = [(7, 4), (6, 5), (6, 6), (6, 7), (6, 3), (6, 2), (6, 1), (6, 0)]
    assert valid_moves == expected_moves
