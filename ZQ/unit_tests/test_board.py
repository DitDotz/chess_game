# import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from board import Board
from pieces import Color, Piece


def test_board_init():
    board = Board()
    assert isinstance(board.board, dict)
    assert board.king_in_checkmate == False
    assert board.moves_made == 0
    assert board.expected_player == Color.WHITE


def test_empty_board():
    board = Board()
    empty_board = board.empty_board()
    assert isinstance(empty_board, dict)
    assert len(empty_board) == 64
    for position, piece in empty_board.items():
        assert isinstance(position, tuple)
        assert isinstance(piece, Piece)


def test_set_correct_player_turn_white():
    # Test for even moves made
    board_even_moves = Board()
    board_even_moves.moves_made = 4
    board_even_moves.set_correct_player_turn()
    assert board_even_moves.expected_player == Color.WHITE


def test_set_correct_player_turn_black():
    # Test for even moves made
    board_even_moves = Board()
    board_even_moves.moves_made = 3
    board_even_moves.set_correct_player_turn()
    assert board_even_moves.expected_player == Color.BLACK


def test_get_all_valid_moves_starting_position_white():
    board = Board()
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    board.process_fen(fen)
    valid_moves = board.get_all_valid_moves(color=Color.WHITE, board=board.board)
    assert len(valid_moves) == 20


def test_get_all_valid_moves_starting_position_black():
    board = Board()
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    board.process_fen(fen)
    valid_moves = board.get_all_valid_moves(color=Color.BLACK, board=board.board)
    assert len(valid_moves) == 20


def test_get_all_valid_moves_double_check_only_king_moves():
    board = Board()
    fen = "3r4/8/8/8/q7/5N2/R7/3K4"
    board.process_fen(fen)
    valid_moves = board.get_all_valid_moves(color=Color.WHITE, board=board.board)
    assert len(valid_moves) == 3


def test_is_king_in_checkmate_no():
    board = Board()
    fen = "3kr3/2p5/3Q4/8/8/8/8/8"
    board.process_fen(fen)
    board.expected_player = Color.BLACK
    board.check_is_king_in_checkmate()

    assert board.king_in_checkmate == False


def test_is_king_in_checkmate_yes():
    board = Board()
    fen = "3k4/3QQ3/8/8/8/8/8/8"
    board.process_fen(fen)
    board.expected_player = Color.BLACK
    board.check_is_king_in_checkmate()
    assert board.king_in_checkmate == False
