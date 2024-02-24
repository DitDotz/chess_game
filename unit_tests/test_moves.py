from typing import Dict, Tuple

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
    KingMovement,
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


def test_KingMovement_within_board_and_valid_directions():
    fen = "8/8/8/8/8/K7/8/8"
    board = Board()
    board.process_fen(fen)
    king = board.board[5, 0]
    king_movement = KingMovement(king)
    valid_moves = king_movement.get_valid_moves(board.board)
    expected_moves = [(4, 0), (4, 1), (5, 1), (6, 0), (6, 1)]
    assert valid_moves == expected_moves


def test_KingMovement_cannot_walk_into_check():
    fen = "2r1r3/8/8/8/3K4/8/8/8"
    board = Board()
    board.process_fen(fen)
    king = board.board[4, 3]
    king_movement = KingMovement(king)
    valid_moves = king_movement.get_valid_moves(board.board)
    expected_moves = [(3, 3), (5, 3)]
    assert valid_moves == expected_moves


def test_KingMovement_has_no_valid_moves():
    fen = "2rrr3/8/8/8/3K4/8/8/8"
    board = Board()
    board.process_fen(fen)
    king = board.board[4, 3]
    king_movement = KingMovement(king)
    valid_moves = king_movement.get_valid_moves(board.board)
    expected_moves = []
    assert valid_moves == expected_moves


# Test RookMovement
def test_RookMovement_valid_moves_along_x_ray_direction():

    fen = "4r3/8/1q5b/8/3RRR2/4K3/4R3/4n3"
    board = Board()
    board.process_fen(fen)
    origin_pos, final_pos_piece = Notation.interpret_notation("Re4e8")
    rook = board.board[origin_pos]
    rook_movement = RookMovement(rook)
    valid_moves = rook_movement.get_valid_moves(board.board)

    expected_moves = [(3, 4), (2, 4), (1, 4), (0, 4)]
    assert valid_moves == expected_moves


def test_RookMovement_can_capture_piece_giving_check():

    board = Board()
    fen = "4r3/8/8/8/q7/8/R2P4/3K4"
    board.process_fen(fen)
    valid_moves = RookMovement(piece=board.board[(6, 0)]).get_valid_moves(
        board=board.board
    )
    expected_moves = [(4, 0), (6, 2)]
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


def test_BishopMovement_can_capture_piece_giving_check():

    board = Board()
    fen = "4r3/8/2B5/8/q7/8/3P4/3K4"
    board.process_fen(fen)
    valid_moves = BishopMovement(piece=board.board[(2, 2)]).get_valid_moves(
        board=board.board
    )
    expected_moves = [(4, 0)]
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


def test_QueenMovement_can_capture_piece_giving_check():

    board = Board()
    fen = "4r3/8/2Q5/8/q7/8/3P4/3K4"
    board.process_fen(fen)
    valid_moves = QueenMovement(piece=board.board[(2, 2)]).get_valid_moves(
        board=board.board
    )
    expected_moves = [(4, 0), (6, 2)]
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


def test_KnightMovement_can_capture_piece_giving_check():

    board = Board()
    fen = "4r3/8/8/2N5/q7/8/3P4/3K4"
    board.process_fen(fen)
    valid_moves = KnightMovement(piece=board.board[(3, 2)]).get_valid_moves(
        board=board.board
    )
    expected_moves = [(5, 1), (4, 0)]
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
def test_PawnMovement_can_capture_piece_giving_check_white():

    board = Board()
    fen = "4r3/8/8/8/8/5q2/3P2P1/3K4"
    board.process_fen(fen)
    valid_moves = PawnMovement(piece=board.board[(6, 6)]).get_valid_moves(
        board=board.board
    )
    expected_moves = [(5, 5)]
    assert valid_moves == expected_moves


def test_PawnMovement_can_capture_piece_giving_check_black():

    board = Board()
    fen = "3kr3/2p5/3Q4/8/8/8/8/8"
    board.process_fen(fen)
    valid_moves = PawnMovement(piece=board.board[(1, 2)]).get_valid_moves(
        board=board.board
    )
    expected_moves = [(2, 3)]
    assert valid_moves == expected_moves


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


def test_is_king_in_check_black_pawn_on_left():
    fen = "8/8/8/8/8/8/2p5/3K4"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.WHITE, board=board.board
        )
        == True
    )


def test_is_king_in_check_black_pawn_on_right():
    fen = "8/8/8/8/8/8/3p4/2K5"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.WHITE, board=board.board
        )
        == True
    )


def test_is_king_in_check_white_pawn_on_left():
    fen = "2k5/1P6/8/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_white_pawn_on_right():
    fen = "2k5/3P4/8/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_rook_vertical():
    fen = "2k5/8/8/8/8/8/8/2R5"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_rook_horizontal():
    fen = "2k4R/8/8/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_bishop_diagonal_1():
    fen = "2k5/8/4B3/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_bishop_diagonal_2():
    fen = "2k5/8/B7/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_queen_vertical():
    fen = "2k5/8/8/8/8/8/8/2Q5"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_queen_horizontal():
    fen = "2k4Q/8/8/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_queen_diagonal_1():
    fen = "2k5/8/4Q3/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_queen_diagonal_2():
    fen = "2k5/8/Q7/8/8/8/8/8"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.BLACK, board=board.board
        )
        == True
    )


def test_is_king_in_check_no_checks():
    fen = "1r6/8/8/5b2/8/8/PPP5/1K6"
    board = Board()
    board.process_fen(fen)
    assert (
        UniversalMovementValidation.is_king_in_check(
            color=Color.WHITE, board=board.board
        )
        == False
    )
