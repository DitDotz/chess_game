from typing import Dict, Tuple
from copy import deepcopy

# import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from board import Board
from pieces import Color


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


# def test_get_all_valid_moves_single_check_king_moves_or_blockable():
# board = Board()
# fen = "8/8/8/5B2/q2N4/8/R7/1Q1K4"
# board.process_fen(fen)
# valid_moves = board.get_all_valid_moves(color=Color.WHITE, board=board.board)
# assert len(valid_moves) == 3
