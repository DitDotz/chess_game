from typing import Dict, Tuple
from copy import deepcopy

# import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from moves import (
    UniversalMovementValidation,
    RookMovement,
    BishopMovement,
    QueenMovement,
    KnightMovement,
    PawnMovement,
)
from pieces import Piece, PieceType, Color
from board import Board
from notation import Notation
from utility import BoardUtils


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
    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Rd4d1")
    piece_to_move = board.board[origin_pos]
    simulated_board = deepcopy(board.board)
    # Simulate the move of the piece on the simulated board in available direction
    BoardUtils.simulate_piece_move(
        simulated_board=simulated_board,
        piece=piece_to_move,
        new_x=final_pos_piece.x,
        new_y=final_pos_piece.y,
    )

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            originalPiece=piece_to_move,
            board=simulated_board,
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
    origin_pos, final_pos_piece = Notation.interpret_notation("Rf4f1")
    piece_to_move = board.board[origin_pos]
    simulated_board = deepcopy(board.board)
    # Simulate the move of the piece on the simulated board in available direction
    BoardUtils.simulate_piece_move(
        simulated_board=simulated_board,
        piece=piece_to_move,
        new_x=final_pos_piece.x,
        new_y=final_pos_piece.y,
    )

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            originalPiece=piece_to_move,
            board=simulated_board,
        )
        == True
    )


def test_is_pinned_to_own_king_can_move_along_x_ray_direction():
    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"

    board = Board()
    print(board)
    board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
    origin_pos, final_pos_piece = Notation.interpret_notation("Re4e6")
    piece_to_move = board.board[origin_pos]
    simulated_board = deepcopy(board.board)
    # Simulate the move of the piece on the simulated board in available direction
    BoardUtils.simulate_piece_move(
        simulated_board=simulated_board,
        piece=piece_to_move,
        new_x=final_pos_piece.x,
        new_y=final_pos_piece.y,
    )

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            originalPiece=piece_to_move,
            board=simulated_board,
        )
        == False
    )


def test_is_pinned_to_own_king_knight_not_involved():
    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"

    board = Board()
    print(board)
    board.process_fen("4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3")
    origin_pos, final_pos_piece = Notation.interpret_notation("Re2a2")
    piece_to_move = board.board[origin_pos]
    simulated_board = deepcopy(board.board)
    # Simulate the move of the piece on the simulated board in available direction
    BoardUtils.simulate_piece_move(
        simulated_board=simulated_board,
        piece=piece_to_move,
        new_x=final_pos_piece.x,
        new_y=final_pos_piece.y,
    )

    assert (
        UniversalMovementValidation.is_pinned_to_own_king(
            originalPiece=piece_to_move,
            board=simulated_board,
        )
        == False
    )


# Test RookMovement
def test_RookMovement_valid_moves_along_x_ray_direction():

    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Re4e6")
    rook = board.board[origin_pos]
    rook_movement = RookMovement(rook)
    valid_moves = rook_movement.get_valid_moves(board.board)

    expected_moves = [(3, 4), (2, 4), (1, 4), (0, 4)]
    assert valid_moves == expected_moves


def test_RookMovement_valid_moves_pinned():

    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Rd4d5")
    rook = board.board[origin_pos]
    rook_movement = RookMovement(rook)
    valid_moves = rook_movement.get_valid_moves(board.board)

    expected_moves = []
    assert valid_moves == expected_moves


def test_RookMovement_valid_moves_capture():

    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Re2e1")
    rook = board.board[origin_pos]
    rook_movement = RookMovement(rook)
    valid_moves = rook_movement.get_valid_moves(board.board)

    expected_moves = [(7, 4), (6, 5), (6, 6), (6, 7), (6, 3), (6, 2), (6, 1), (6, 0)]
    assert valid_moves == expected_moves


def test_BishopMovement_valid_moves_pinned():

    fen = "4r3/8/1q5b/8/3BBB2/4K3/4B3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Be4d3")
    bishop = board.board[origin_pos]
    bishop_movement = BishopMovement(bishop)
    valid_moves = bishop_movement.get_valid_moves(board.board)

    expected_moves = []
    assert valid_moves == expected_moves


def test_BishopMovement_valid_moves_along_x_ray_direction():

    fen = "4r3/8/1q5b/8/3BBB2/4K3/4B3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Bf4g5")
    bishop = board.board[origin_pos]
    bishop_movement = BishopMovement(bishop)
    valid_moves = bishop_movement.get_valid_moves(board.board)

    expected_moves = [(3, 6), (2, 7)]
    assert valid_moves == expected_moves


def test_BishopMovement_valid_moves_capture_along_x_ray():
    fen = "4r3/8/1q5b/8/3BBB2/4K3/4B3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Bd4b6")
    bishop = board.board[origin_pos]
    bishop_movement = BishopMovement(bishop)
    valid_moves = bishop_movement.get_valid_moves(board.board)

    expected_moves = [(3, 2), (2, 1)]
    assert valid_moves == expected_moves


def test_QueenMovement_valid_moves_capture_along_x_ray_diagonal():
    fen = "4r3/8/1q5b/8/3QQQ2/4K3/4Q3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Qd4b6")
    queen = board.board[origin_pos]
    queen_movement = QueenMovement(queen)
    valid_moves = queen_movement.get_valid_moves(board.board)

    expected_moves = [(3, 2), (2, 1)]
    assert valid_moves == expected_moves


def test_QueenMovement_valid_moves_capture_along_x_ray_vertical():

    fen = "4r3/8/1q5b/8/3QQQ2/4K3/4Q3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Qe4d3")
    queen = board.board[origin_pos]
    queen_movement = QueenMovement(queen)
    valid_moves = queen_movement.get_valid_moves(board.board)

    expected_moves = [(3, 4), (2, 4), (1, 4), (0, 4)]
    assert valid_moves == expected_moves


def test_QueenMovement_valid_moves_no_pins():
    fen = "4r3/8/1q5b/8/3QQQ2/4K3/4Q3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Qe2e1")
    queen = board.board[origin_pos]
    queen_movement = QueenMovement(queen)
    valid_moves = queen_movement.get_valid_moves(board.board)
    expected_moves = [
        (5, 3),
        (4, 2),
        (3, 1),
        (2, 0),
        (5, 5),
        (4, 6),
        (3, 7),
        (6, 3),
        (6, 2),
        (6, 1),
        (6, 0),
        (6, 5),
        (6, 6),
        (6, 7),
        (7, 3),
        (7, 4),
        (7, 5),
    ]
    assert valid_moves == expected_moves


# Test KnightMovement
def test_KnightMovement_valid_moves_no_pins():
    fen = "4r3/8/1q5b/8/3NNN2/4K3/4N3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Ne2e1")
    knight = board.board[origin_pos]
    knight_movement = KnightMovement(knight)
    valid_moves = knight_movement.get_valid_moves(board.board)
    expected_moves = [(7, 6), (7, 2), (5, 6), (5, 2)]
    assert valid_moves == expected_moves


def test_KnightMovement_valid_moves_pinned():
    fen = "4r3/8/1q5b/8/3NNN2/4K3/4N3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Ne4f6")
    knight = board.board[origin_pos]
    knight_movement = KnightMovement(knight)
    valid_moves = knight_movement.get_valid_moves(board.board)
    expected_moves = []
    assert valid_moves == expected_moves


# test PawnMovement
def test_PawnMovement_black_not_moved_and_capture():
    fen = "4k3/3p1p2/4P3/pP5B/6pP/3b4/2P2P2/1K6"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("pd7d6")
    pawn = board.board[origin_pos]
    pawn_movement = PawnMovement(pawn)
    valid_moves = pawn_movement.get_valid_moves(board.board)
    expected_moves = [(2, 3), (3, 3), (2, 4)]
    assert valid_moves == expected_moves


def test_PawnMovement_white_not_moved():
    fen = "4k3/3p1p2/4P3/pP5B/6pP/3b4/2P2P2/1K6"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Pf2f3")
    pawn = board.board[origin_pos]
    pawn_movement = PawnMovement(pawn)
    valid_moves = pawn_movement.get_valid_moves(board.board)
    expected_moves = [(5, 5), (4, 5)]
    assert valid_moves == expected_moves


def test_PawnMovement_is_pinned():
    fen = "4k3/3p1p2/4P3/pP5B/6pP/3b4/2P2P2/1K6"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("pf7e6")
    pawn = board.board[origin_pos]
    pawn_movement = PawnMovement(pawn)
    valid_moves = pawn_movement.get_valid_moves(board.board)
    expected_moves = []
    assert valid_moves == expected_moves


def test_PawnMovement_white_en_passantable_after_double_move():
    fen = "4k3/3p1p2/4P3/pP5B/6pP/3b4/2P2P2/1K6"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("pg4h3")
    board.board[(4, 7)].en_passantable = True
    pawn = board.board[origin_pos]
    pawn_movement = PawnMovement(pawn)
    valid_moves = pawn_movement.get_valid_moves(board.board)
    expected_moves = [(5, 6), (5, 7)]
    assert valid_moves == expected_moves


def test_PawnMovement_black_en_passantable_after_double_move():
    fen = "4k3/3p1p2/4P3/pP5B/6pP/3b4/2P2P2/1K6"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Pb5a6")
    board.board[(3, 0)].en_passantable = True
    pawn = board.board[origin_pos]
    pawn_movement = PawnMovement(pawn)
    valid_moves = pawn_movement.get_valid_moves(board.board)
    expected_moves = [(2, 1), (2, 0)]
    assert valid_moves == expected_moves


def test_PawnMovement_capture_along_x_ray_direction():
    fen = "4k3/3p1p2/4P3/pP5B/6pP/3b4/2P2P2/1K6"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Pc2d3")
    pawn = board.board[origin_pos]
    pawn_movement = PawnMovement(pawn)
    valid_moves = pawn_movement.get_valid_moves(board.board)
    expected_moves = [(5, 3)]
    assert valid_moves == expected_moves
